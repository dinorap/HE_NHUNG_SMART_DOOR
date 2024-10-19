import cv2
import os
import time
import dlib
from display import DisplayScreen
from train_model import train_face_recognition

def capture_and_train(username):
    """
    Hàm này dùng để chụp ảnh khuôn mặt của người dùng và sau đó bắt đầu quá trình train model.
    
    Parameters:
    username (str): Tên của người dùng sẽ được sử dụng để lưu trữ và train model nhận diện khuôn mặt.
    """
    
    # Tạo đối tượng màn hình hiển thị
    display = DisplayScreen()

    # Tạo thư mục lưu trữ nếu chưa tồn tại
    dataset_dir = f"dataset/{username}"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)  # Tạo thư mục nếu chưa có

    # Tìm số lượng ảnh đã lưu
    existing_images = len([name for name in os.listdir(dataset_dir) if name.endswith('.jpg')])
    img_counter = existing_images  # Đếm số ảnh đã có
    display.add_message("Ấn space để bắt đầu chụp ảnh")  # Hiển thị thông báo yêu cầu bắt đầu chụp ảnh

    # Khởi tạo camera
    cam = cv2.VideoCapture(0)

    # Khởi tạo dlib face detector
    detector = dlib.get_frontal_face_detector()

    # Tạo cửa sổ để hiển thị quá trình chụp ảnh
    cv2.namedWindow("Capturing Photos...", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Capturing Photos...", 500, 300)

    num_photos = 100  # Số lượng ảnh cần chụp
    capture_delay = 0.1  # Delay giữa các lần chụp ảnh

    print(f"Press SPACE to start capturing {num_photos} photos... or ESC to exit.")

    # Biến để điều khiển trạng thái chụp ảnh
    is_capturing = False

    while img_counter < existing_images + num_photos:  # Lặp cho đến khi đủ số ảnh cần chụp
        ret, frame = cam.read()  # Đọc khung hình từ camera
        if not ret:
            print("Failed to grab frame")  # Thông báo nếu không đọc được khung hình
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Chuyển đổi khung hình sang ảnh xám

        # Phát hiện khuôn mặt
        faces = detector(gray)
        print(f"Detected faces: {len(faces)}")  # In ra số lượng khuôn mặt phát hiện được

        # Vẽ hình chữ nhật quanh các khuôn mặt phát hiện được
        for (i, face) in enumerate(faces):
            cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (255, 0, 0), 2)

        # Hiển thị khung hình camera
        cv2.imshow("Capturing Photos...", frame)

        # Kiểm tra phím nhấn
        k = cv2.waitKey(1) & 0xFF

        if k == 27:  # ESC để thoát
            print("Escape hit, closing...")
            break
        elif k == ord('q'):  # q để thoát hoàn toàn không chụp và không train
            print("Q hit, quitting without capturing or training...")
            display.clear_message()  # Xóa thông báo hiển thị
            cam.release()  # Giải phóng camera
            cv2.destroyAllWindows()  # Đóng tất cả cửa sổ
        elif k == 32:  # SPACE để bắt đầu hoặc tạm dừng chụp ảnh
            is_capturing = not is_capturing  # Chuyển đổi trạng thái chụp
            if is_capturing:
                print("Started capturing photos...")  # Thông báo bắt đầu chụp
            else:
                print("Paused capturing photos...")  # Thông báo tạm dừng chụp

        # Nếu đang trong chế độ chụp và phát hiện 1 khuôn mặt
        if is_capturing and len(faces) == 1:
            img_name = f"{dataset_dir}/image_{img_counter}.jpg"  # Tạo tên tệp cho ảnh
            cv2.imwrite(img_name, frame)  # Lưu ảnh vào thư mục
            print(f"{img_name} written!")  # Thông báo đã lưu ảnh
            img_counter += 1  # Tăng số lượng ảnh đã chụp
            time.sleep(capture_delay)  # Delay giữa các lần chụp ảnh
        elif is_capturing and len(faces) > 1:
            print("More than one face detected! Please move to a clearer position.")  # Thông báo khi phát hiện nhiều khuôn mặt
        elif is_capturing and len(faces) == 0:
            print("No face detected! Please move to a clearer position.")  # Thông báo khi không phát hiện khuôn mặt

    # Giải phóng camera và đóng tất cả cửa sổ
    cam.release()  # Giải phóng camera
    cv2.destroyAllWindows()  # Đóng tất cả cửa sổ
    print("Done capturing photos.")  # Thông báo hoàn thành quá trình chụp ảnh
    display.add_message("Chụp hình hoàn tất")  # Hiển thị thông báo hoàn tất

    # Bắt đầu train sau khi chụp xong
    train_face_recognition(username)  # Gọi hàm huấn luyện mô hình nhận diện khuôn mặt
    print("Training complete.")  # Thông báo hoàn thành quá trình huấn luyện
