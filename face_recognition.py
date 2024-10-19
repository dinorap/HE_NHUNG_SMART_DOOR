import dlib
import cv2
import numpy as np
import time
from imutils.video import VideoStream
from gpio_setup import *
import os
import pickle
from scipy.spatial import distance  # Thư viện để tính khoảng cách
from display import *  # Nhập hàm để hiển thị thông báo vào giao diện
import threading
from send_email import *

unknown_count = 0
unknown_threshold = 100

# Khởi tạo bộ phát hiện khuôn mặt của dlib và tạo một encoder
detector = dlib.get_frontal_face_detector()  # Bộ phát hiện khuôn mặt
sp = dlib.shape_predictor("Model/shape_predictor_68_face_landmarks.dat")  # Dự đoán các điểm đặc trưng trên khuôn mặt
face_encoder = dlib.face_recognition_model_v1("Model/dlib_face_recognition_resnet_model_v1.dat")  # Mô hình nhận diện khuôn mặt

# Tạo thư mục Warning nếu chưa tồn tại
warning_folder = "Warning"
if not os.path.exists(warning_folder):
    os.makedirs(warning_folder)

def load_known_faces(train_directory="train"):
    """
    Tải các khuôn mặt đã biết từ thư mục.
    
    Parameters:
    train_directory (str): Thư mục chứa dữ liệu khuôn mặt đã được huấn luyện.
    
    Returns:
    data (dict): Chứa danh sách encoding và tên khuôn mặt.
    """
    data = {"encodings": [], "names": []}  # Khởi tạo dữ liệu lưu trữ encoding và tên
    for filename in os.listdir(train_directory):
        if filename.endswith("_encodings.pickle"): 
            file_path = os.path.join(train_directory, filename)
            with open(file_path, "rb") as f:
                file_data = pickle.loads(f.read())  # Tải dữ liệu từ tệp
                data["encodings"].extend(file_data["encodings"])  
                data["names"].extend(file_data["names"])
    return data

def save_unknown_face(frame):
    """
    Lưu hình ảnh khuôn mặt không xác định vào thư mục Warning với tên hợp lệ.
    
    Parameters:
    frame (ndarray): Khung hình hiện tại chứa khuôn mặt không xác định.
    """
    base_filename = "intruder"
    count = 0
    filename = os.path.join(warning_folder, f"{base_filename}.jpg")

    # Kiểm tra xem tệp đã tồn tại chưa và thay đổi tên nếu cần
    while os.path.exists(filename):
        count += 1
        filename = os.path.join(warning_folder, f"{base_filename}{count}.jpg")
    
    cv2.imwrite(filename, frame)  # Lưu khung hình vào tệp
    return filename

def unlock_with_face(data):
    global unknown_count, unknown_threshold
    """
    Mở khóa cửa bằng khuôn mặt nếu được nhận diện.
    
    Parameters:
    data (dict): Dữ liệu chứa các encoding và tên khuôn mặt đã biết.
    """
    if data is None or len(data["encodings"]) == 0:
        show_message("Không có dữ liệu khuôn mặt")  # Hiển thị thông báo nếu không có dữ liệu khuôn mặt
        return  # Thoát nếu không có dữ liệu khuôn mặt
    
    show_message("Camera đang khởi động")  # Hiển thị thông báo bắt đầu video stream
    vs = VideoStream(src=0).start()  # Khởi động camera
    time.sleep(2.0)  # Delay cho camera khởi động
    doorUnlock = False
    prevTime = 0
    frame_skip = 1  # Bỏ qua khung hình để cải thiện hiệu suất
    frame_count = 0
    last_recognition_time = 0  # Thời gian nhận diện cuối cùng
    recognition_cooldown = 15  # Thời gian trước khi nhận diện lại (15 giây)

    while True:
        frame = vs.read()  # Đọc khung hình từ video stream

        # Gọi hàm kiểm tra nút bấm
        check_button()  # Đảm bảo kiểm tra nút bấm luôn luôn được thực hiện

        # Chỉ xử lý mỗi frame_skip-th frame
        frame_count += 1
        if frame_count % frame_skip != 0:
            continue  # Bỏ qua các frame không cần thiết

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đổi khung hình sang định dạng RGB

        # Phát hiện khuôn mặt trong khung hình
        dets = detector(rgb, 1)  # Phát hiện khuôn mặt
        encodings, names = [], []  # Danh sách lưu encoding và tên khuôn mặt

        for d in dets:
            shape = sp(rgb, d)  # Dự đoán các điểm đặc trưng trên khuôn mặt
            encoding = face_encoder.compute_face_descriptor(rgb, shape)  # Tính encoding khuôn mặt
            encoding = np.array(encoding)  # Chuyển đổi encoding thành mảng numpy
            encodings.append(encoding)  # Thêm encoding vào danh sách

            name = "Unknown"  # Mặc định tên là Unknown
            
            # Tối ưu hóa tính toán khoảng cách bằng scipy's spatial distance
            distances = distance.cdist([encoding], data["encodings"], "euclidean")  # Tính khoảng cách
            min_distance = np.min(distances)  # Khoảng cách nhỏ nhất
            min_index = np.argmin(distances)  # Chỉ số của khoảng cách nhỏ nhất
            
            if min_distance < 0.3:  # Điều chỉnh ngưỡng theo nhu cầu
                name = data["names"][min_index]  # Lấy tên tương ứng

            names.append(name)  # Thêm tên vào danh sách
            if name == "Unknown":
                unknown_count += 1  # Tăng biến đếm khi gặp "Unknown"
                # Lưu hình ảnh và gửi email nếu gặp nhiều "Unknown"
                
                if unknown_count > unknown_threshold:
                    save_unknown_face(frame)  # Lưu khung hình hiện tại\
                    image_path=save_unknown_face(frame)
                    SendEmail1(os.path.join(image_path))  # Gọi hàm gửi email cảnh báo với hình ảnh đính kèm
                    unknown_count = 0  # Reset biến đếm sau khi gửi email
            else:
                unknown_count = 0  # Reset nếu nhận diện thành công

            # Kiểm tra xem có đủ thời gian để nhận diện lại không
            if name != "Unknown" and (time.time() - last_recognition_time) > recognition_cooldown:
                unlock_door()  # Mở khóa cửa
                prevTime = time.time()  # Cập nhật thời gian hiện tại
                doorUnlock = True
                activate_correct_alarm()  # Kích hoạt báo thức đúng
                threading.Timer(3.0, deactivate_alarm).start()  # Kích hoạt báo thức sau 3 giây
                last_recognition_time = time.time()  # Cập nhật thời gian nhận diện

        # Khóa cửa sau khoảng thời gian nhận diện lại
        if get_door_status() == False:  # Kiểm tra trạng thái cửa
            if get_prevTime1() > prevTime:  # Cập nhật thời gian
                prevTime = get_prevTime1()
            if doorUnlock and len(dets) == 0 and time.time() - prevTime > 15:  # Nếu không có khuôn mặt
                doorUnlock = False
                lock_door()  # Khóa cửa
                show_message("Cửa đã khóa")  # Hiển thị thông báo cửa đã khóa

        # Vẽ hình chữ nhật quanh khuôn mặt và hiển thị tên
        for (d, name) in zip(dets, names):
            (x, y, w, h) = (d.left(), d.top(), d.right(), d.bottom())
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)  # Vẽ hình chữ nhật quanh khuôn mặt
            cv2.putText(frame, name, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)  # Hiển thị tên khuôn mặt

        # Hiển thị trạng thái khóa/mở khóa
        status_text = "Unlock" if doorUnlock else "Lock"
        status_color = (0, 255, 0) if doorUnlock else (0, 0, 255)  # Màu sắc cho trạng thái
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)  # Hiển thị trạng thái

        cv2.imshow("Nhận diện khuôn mặt", frame)  # Hiển thị khung hình

        # Thoát vòng lặp nếu nhấn 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            display.clear_message()  # Xóa thông báo
            turn_off_relay()  # Tắt relay
            break  # Thoát vòng lặp

    vs.stop()  # Dừng video stream
    cv2.destroyAllWindows()  # Đóng tất cả cửa sổ
