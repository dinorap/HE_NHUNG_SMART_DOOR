from imutils import paths  # Thư viện hỗ trợ xử lý ảnh
import dlib  # Thư viện nhận diện khuôn mặt
import pickle  # Thư viện để lưu trữ dữ liệu
import cv2  # Thư viện xử lý ảnh
import os  # Thư viện thao tác với hệ thống tệp
from display import DisplayScreen  # Thư viện hiển thị thông báo
import tkinter as tk  # Thư viện GUI
from tkinter import messagebox  # Thư viện hiển thị hộp thoại thông báo

def train_face_recognition(username):
    """
    Hàm này dùng để train dữ liệu khuôn mặt của người dùng và lưu kết quả mã hóa khuôn mặt vào file pickle.
    
    Parameters:
    username (str): Tên của người dùng sẽ được sử dụng để train model nhận diện khuôn mặt.
    """
    display = DisplayScreen()  # Khởi tạo đối tượng để hiển thị thông báo
    display.add_message("Bắt đầu train dữ liệu")  # Thông báo bắt đầu quá trình train

    # Khởi tạo bộ phát hiện khuôn mặt và encoder của dlib
    detector = dlib.get_frontal_face_detector()  # Bộ phát hiện khuôn mặt
    sp = dlib.shape_predictor("Model/shape_predictor_68_face_landmarks.dat")  # Tải mô hình landmarks để xác định các điểm trên khuôn mặt
    face_encoder = dlib.face_recognition_model_v1("Model/dlib_face_recognition_resnet_model_v1.dat")  # Tải mô hình nhận diện khuôn mặt

    # Đường dẫn đến thư mục chứa hình ảnh của người dùng
    dataset_dir = os.path.join("dataset", username)  # Chỉ định thư mục dựa trên tên người dùng
    print("[INFO] Start processing faces...")  # In ra thông báo bắt đầu xử lý
    imagePaths = list(paths.list_images(dataset_dir))  # Lấy danh sách hình ảnh từ thư mục người dùng

    # Khởi tạo danh sách mã hóa và tên đã biết
    knownEncodings = []  # Danh sách lưu mã hóa khuôn mặt
    knownNames = []  # Danh sách lưu tên người dùng

    # Duyệt qua các đường dẫn hình ảnh
    for (i, imagePath) in enumerate(imagePaths):
        print("[INFO] Processing image {}/{}".format(i + 1, len(imagePaths)))  # In ra thông báo đang xử lý hình ảnh nào
        
        # Load hình ảnh và chuyển đổi từ BGR sang RGB
        image = cv2.imread(imagePath)  # Đọc hình ảnh từ file
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Chuyển đổi màu sắc

        # Phát hiện khuôn mặt trong hình ảnh
        dets = detector(rgb, 1)  # Phát hiện khuôn mặt

        # Duyệt qua các khuôn mặt đã phát hiện
        for d in dets:
            # Lấy các landmarks và tính toán mã hóa khuôn mặt
            shape = sp(rgb, d)  # Lấy các điểm landmarks của khuôn mặt
            encoding = face_encoder.compute_face_descriptor(rgb, shape)  # Tính toán mã hóa khuôn mặt

            # Thêm mỗi mã hóa + tên vào tập hợp các tên và mã hóa đã biết
            knownEncodings.append(encoding)  # Thêm mã hóa vào danh sách
            knownNames.append(username)  # Thêm tên người dùng vào danh sách

    # Lưu các mã hóa và tên vào file pickle theo tên người dùng
    print("[INFO] Serializing encodings...")  # In ra thông báo bắt đầu lưu dữ liệu
    data = {"encodings": knownEncodings, "names": knownNames}  # Tạo dictionary chứa dữ liệu

    # Lưu file pickle vào thư mục "train"
    output_dir = "train"  # Đường dẫn đến thư mục train
    os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

    # Đặt đường dẫn cho file pickle
    pickle_file_path = os.path.join(output_dir, f"{username}_encodings.pickle")  # Tạo đường dẫn cho file pickle
    with open(pickle_file_path, "wb") as f:  # Mở file để ghi dữ liệu
        f.write(pickle.dumps(data))  # Ghi dữ liệu vào file pickle

    # Hiển thị thông báo hoàn tất trên màn hình
    display.add_message("Train hoàn tất")  # Thông báo hoàn tất train
    display.add_message(f"[INFO] Encodings serialized to {pickle_file_path}")  # Thông báo đường dẫn file pickle

    # Đóng cửa sổ sau khi hoàn thành
    root = tk.Tk()  # Tạo một cửa sổ Tkinter mới
    root.withdraw()  # Ẩn cửa sổ chính
    messagebox.showinfo("Thông báo", "Hoàn tất train dữ liệu!")  # Hiển thị thông báo hoàn tất
    print("Hoàn tất train dữ liệu!")  # Dòng in ra để kiểm tra
