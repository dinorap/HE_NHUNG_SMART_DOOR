# Mô Tả Dự Án

Dự án này là một hệ thống mở khóa đa dạng, cho phép người dùng mở khóa thông qua nhận diện khuôn mặt, mật khẩu, hoặc thẻ RFID. Giao diện người dùng được xây dựng bằng Tkinter, và dữ liệu khuôn mặt được mã hóa và lưu trữ để sử dụng trong quá trình xác thực. 

## Chức Năng

### Mở khóa bằng khuôn mặt:
- Nhận diện khuôn mặt người dùng và mở khóa nếu nhận diện thành công.
- Sử dụng thư viện **dlib** để phát hiện khuôn mặt và tính toán mã hóa khuôn mặt.

### Mở khóa bằng mật khẩu:
- Cho phép người dùng nhập mật khẩu để mở khóa.
- Sử dụng `tkinter.simpledialog` để thu thập thông tin từ người dùng.

### Mô phỏng đầu vào RFID:
- Cho phép người dùng mô phỏng việc quét thẻ RFID và lưu trữ thông tin thẻ vào file.
- Giao diện đồ họa cho phép kéo thẻ RFID và hiển thị thông tin.

### Quản lý người dùng (Admin):
- Cho phép quản trị viên thêm khuôn mặt và thẻ RFID vào hệ thống.

### Gửi Email cảnh báo:
- Khi có người lạ , nhập mật khẩu sai quá nhiều , hoạc quét thẻ sai quá nhiều thì gửi cảnh báo về cho người dùng 

### Dọn dẹp GPIO:
- Thực hiện các thao tác dọn dẹp GPIO khi chương trình kết thúc.

## Thư Viện Sử Dụng
- **tkinter**: Thư viện giao diện người dùng cho Python.
- **dlib**: Thư viện nhận diện khuôn mặt.
- **cv2 (OpenCV)**: Thư viện xử lý hình ảnh.
- **pickle**: Thư viện để lưu trữ và đọc dữ liệu nhị phân.
- **os**: Thư viện để thao tác với hệ thống tệp.
- **time**: Thư viện để xử lý thời gian.
- **pygame**: Thư viện hỗ trợ phát triển game (không được sử dụng trong mã hiện tại nhưng có thể được sử dụng trong tương lai).
- **EmailMessage**: Thư viện hỗ trợ gửi mail

## Cài Đặt Thư Viện
Để cài đặt các thư viện cần thiết, bạn có thể sử dụng pip. Dưới đây là các lệnh cài đặt:

```bash
pip install dlib
pip install opencv-python
pip install imutils
pip install pygame
```
# Cách Sử Dụng
1. Chạy api.py: Nếu dự án yêu cầu một API để xử lý các yêu cầu từ giao diện người dùng, hãy chạy tệp này trước.
```bash
python api.py
```
2. Chạy main.py: Sau khi API đang chạy, bạn có thể khởi động giao diện người dùng
```bash
python main.py
```
3. Chọn phương thức mở khóa mong muốn: Từ giao diện người dùng, hãy chọn cách mở khóa bạn muốn sử dụng (khuôn mặt, mật khẩu, RFID).
4. Thực hiện các thao tác theo hướng dẫn trên giao diện.

# Ghi Chú
- Đảm bảo rằng bạn đã cài đặt các thư viện phù hợp và cấu hình môi trường Python của bạn trước khi chạy chương trình.
- Bạn cần chuẩn bị các file mô hình cho dlib và đảm bảo rằng đường dẫn đến các file đó là chính xác.

# Kết Luận
- Dự án này cung cấp một hệ thống mở khóa đơn giản nhưng hiệu quả, cho phép người dùng sử dụng nhiều phương thức khác nhau để mở khóa. Các chức năng có thể được mở rộng và cải thiện theo nhu cầu của người dùng.


# 1. Thư mục chính
- dataset/: Chứa dữ liệu liên quan đến hình ảnh khuôn mặt của người dùng, phục vụ cho việc huấn luyện mô hình nhận diện.
- Font/: Chứa các file font chữ cần thiết để hiển thị trên giao diện, ví dụ cho giao diện Tkinter.
- GPIO/: Thư mục này chứa các module điều khiển chân GPIO của Raspberry Pi (mô phỏng).
- Model/: Chứa mô hình máy học, bao gồm mô hình huấn luyện nhận diện khuôn mặt.
- RFID/: Chứa các file liên quan đến đọc và ghi dữ liệu thẻ RFID.
- Sound/: Thư mục chứa âm thanh thông báo khi thao tác mở khóa thành công hoặc thất bại.
- train/: Thư mục chứa các file và dữ liệu đã được huấn luyện nhận dạng 
- Warning/: Thư mục này lưu trữ các file ảnh của những người lạ cố gắng đột nhập vào nhà .
# 2. Các file Python chính
- admin_functions.py: Chứa các hàm dành cho quản trị viên,  bao gồm các chức năng, đăng ký thêm người mới vào hệ thống,thêm thẻ rfid mới v.v.
- api.py: Chứa các hàm liên quan đến API, sử dụng để giao tiếp với các hệ thống bên ngoài, gửi yêu cầu hoặc nhận phản hồi.
- display.py: Chứa các hàm để hiển thị thông báo hoặc giao diện người dùng thông qua giao diện đồ họa như pygame (mô phỏng led lcd)
- face_auto_shot.py: Chứa logic để tự động chụp ảnh khuôn mặt, sử dụng camera để thu thập dữ liệu khuôn mặt phục vụ cho nhận diện.
- face_recognition.py: Chứa logic chính để thực hiện nhận diện khuôn mặt, sử dụng các thư viện như OpenCV và dlib để so sánh và xác thực khuôn mặt.
- gpio_setup.py: Chứa các hàm thiết lập GPIO trên Raspberry Pi, bao gồm định nghĩa các chân GPIO, bật/tắt relay, nút bấm, LED, còi báo, v.v.
- main.py: Tệp chính điều khiển chương trình. Đây là tệp khởi động, quản lý luồng công việc chính của hệ thống, và điều khiển toàn bộ quá trình.
- password_unlock.py: Chứa logic để mở khóa cửa dựa trên mật khẩu, bao gồm việc nhập và kiểm tra mật khẩu của người dùng.
- rfid_simulation.py: Mô phỏng chức năng đọc và ghi thẻ RFID, để kiểm tra hoặc thử nghiệm hệ thống mà không cần phần cứng RFID thật.
- send_email.py: Chứa hàm gửi email, sử dụng để gửi thông báo tới quản trị viên khi có sự cố hoặc yêu cầu mở khóa.
- train_model.py: Chứa logic để huấn luyện mô hình nhận diện khuôn mặt dựa trên dữ liệu hình ảnh thu thập được từ thư mục dataset/.
- write_rfid.py: Chứa logic để ghi dữ liệu lên thẻ RFID,bao gồm việc lưu thông tin người dùng vào thẻ để kiểm tra quyền truy cập.