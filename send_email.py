from email.message import EmailMessage

import smtplib
import os
import cv2
def capture_image():
    """Hàm để chụp ảnh từ camera và lưu vào file với tên duy nhất."""
    # Tạo thư mục warning nếu chưa tồn tại
    os.makedirs('Warning', exist_ok=True)

    # Tìm số thứ tự lớn nhất đã tồn tại trong thư mục warning
    existing_files = [f for f in os.listdir('warning') if f.startswith('intruder')]
    existing_numbers = []
    for file in existing_files:
        if file.endswith('.jpg'):
            number_str = file[len('intruder'):-len('.jpg')]
            if number_str.isdigit():
                existing_numbers.append(int(number_str))

    # Tính số thứ tự tiếp theo
    next_number = max(existing_numbers) + 1 if existing_numbers else 1
    image_path = f"warning/intruder{next_number}.jpg"  # Đặt tên file cho ảnh mới

    # Chụp ảnh từ camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không thể mở camera")
        return None
    
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(image_path, frame)  # Lưu ảnh vào file
    cap.release()
    return image_path  # Trả về đường dẫn ảnh


def SendEmail():
    """Gửi email cảnh báo và đính kèm ảnh."""
    sender_email = "vhau1010@gmail.com"
    sender_password = "uyinfhebgajavqab"
    Receiver_Email = "dminhphuong97@gmail.com"

    # Tạo nội dung email
    newMessage = EmailMessage()
    newMessage['Subject'] = "CẢNH BÁO !!!"
    newMessage['From'] = sender_email
    newMessage['To'] = Receiver_Email
    newMessage.set_content('Cảnh báo: Đã có người nhập sai mật khẩu nhiều lần!')

    # Đính kèm ảnh nếu có
    image_path = capture_image()  # Chụp ảnh từ camera
    if image_path:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            newMessage.add_attachment(image_data, maintype='image', subtype='jpeg', filename=os.path.basename(image_path))

    # Gửi email qua máy chủ Gmail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(newMessage)

def SendEmail1(path):
    """Gửi email cảnh báo và đính kèm ảnh."""
    sender_email = "vhau1010@gmail.com"
    sender_password = "uyinfhebgajavqab"
    Receiver_Email = "dminhphuong97@gmail.com"

    # Tạo nội dung email
    newMessage = EmailMessage()
    newMessage['Subject'] = "CẢNH BÁO !!!"
    newMessage['From'] = sender_email
    newMessage['To'] = Receiver_Email
    newMessage.set_content('Cảnh báo: Có người lạ cố gắng mở cửa nhà bạn')

    # Đính kèm ảnh nếu có
    image_path = path  # Chụp ảnh từ camera
    if image_path:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            newMessage.add_attachment(image_data, maintype='image', subtype='jpeg', filename=os.path.basename(image_path))

    # Gửi email qua máy chủ Gmail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(newMessage)