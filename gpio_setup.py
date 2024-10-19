from GPIO.EmulatorGUI import GPIO  # Nhập thư viện GPIO cho điều khiển phần cứng
import time
from display import show_message  # Nhập hàm để hiển thị thông báo vào giao diện
import pygame  # Nhập thư viện pygame để xử lý âm thanh

# Định nghĩa các chân GPIO
RELAY_PIN = 17  # Sử dụng chân GPIO 17 cho relay
BUTTON_PIN = 27  # Nút bấm mở cửa
SCAN_STATUS_PIN = 18  # Chân để hiển thị trạng thái quét thẻ
DOOR_STATUS_PIN = 15  # Chân để hiển thị trạng thái cửa mở
ALARM_PIN = 22  # Sử dụng chân GPIO 22 cho còi báo động
UNLOCK_PIN=23
door_open = False  # Trạng thái của cửa (đã mở hay chưa)
unlock = False  # Trạng thái mở khóa
prevTime1 = 0  # Thời gian cuối cùng trạng thái cửa thay đổi
pygame.mixer.init()  # Khởi động pygame mixer để phát âm thanh
khoa = True
# Nạp file âm thanh
correct_alarm_sound = pygame.mixer.Sound("Sound/beep-06.wav")  # Âm thanh cho mở khóa đúng
incorrect_alarm_sound = pygame.mixer.Sound("Sound/beep-03.wav")  # Âm thanh cho mở khóa sai

# Thiết lập GPIO
def gpio_setup():
    GPIO.setwarnings(False)  # Tắt cảnh báo
    GPIO.setmode(GPIO.BCM)  # Sử dụng chế độ chân BCM
    GPIO.setup(RELAY_PIN, GPIO.OUT)  # Thiết lập chân relay là đầu ra
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Khởi động relay ở trạng thái LOW
    GPIO.setup(SCAN_STATUS_PIN, GPIO.OUT)  # Thiết lập chân quét thẻ là đầu ra
    GPIO.output(SCAN_STATUS_PIN, GPIO.LOW)  # Ban đầu, trạng thái quét thẻ là không hoạt động (LOW)
    GPIO.setup(DOOR_STATUS_PIN, GPIO.OUT)  # Thiết lập chân trạng thái cửa là đầu ra
    GPIO.output(DOOR_STATUS_PIN, GPIO.LOW)  # Ban đầu, trạng thái cửa là đóng
    GPIO.setup(ALARM_PIN, GPIO.OUT)  # Thiết lập chân alarm
    GPIO.output(ALARM_PIN, GPIO.LOW)  # Khởi động với còi báo động tắt
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Cấu hình nút với pull-up
    GPIO.setup(UNLOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Cấu hình nút với pull-up

# Chuyển đổi trạng thái cửa
def toggle_door_status():
    global door_open, prevTime1
    if door_open:  # Nếu cửa đang mở
        GPIO.output(DOOR_STATUS_PIN, GPIO.LOW)  # Đóng cửa
        show_message("Cửa đã đóng lại.")  # Hiển thị thông báo
        prevTime1 = time.time()  # Cập nhật thời gian
        door_open = not door_open  # Đảo ngược trạng thái cửa
    else:  # Nếu cửa đang đóng
        GPIO.output(DOOR_STATUS_PIN, GPIO.HIGH)  # Mở cửa
        show_message("Cửa đã mở hẳn.")  # Hiển thị thông báo
        prevTime1 = time.time()  # Cập nhật thời gian
        door_open = not door_open  # Đảo ngược trạng thái cửa

# Kiểm tra trạng thái nút bấm và chuyển đổi trạng thái cửa nếu điều kiện thỏa mãn
def check_button():
    if unlock:  # Chỉ cho phép nhấn nút nếu cửa đã được mở khóa
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Nút bấm được nhấn
            if door_open:  # Nếu cửa đang mở
                show_message("Đang đóng cửa")  # Hiển thị thông báo
                toggle_door_status()  # Chuyển đổi trạng thái cửa
            else:  # Nếu cửa đang đóng
                show_message("Đang mở cửa")  # Hiển thị thông báo
                toggle_door_status()  # Chuyển đổi trạng thái cửa
            time.sleep(0.2)  # Độ trễ ngắn để chống rung
def button_unlock():
    global khoa
    if GPIO.input(UNLOCK_PIN) == GPIO.LOW:
        if khoa:
            khoa= False
            lock_door()
        else:
            khoa= True
            unlock_door()
        
def check_u():
    show_message("Cửa đã được mở khóa. Vui lòng thử lại sau.")

# Các hàm mở và khóa cửa
def unlock_door():
    global unlock 
    unlock = True  # Đặt trạng thái mở khóa là True
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Mở khóa cửa và kích hoạt relay
    show_message("Cửa đã được mở khóa.")  # Hiển thị thông báo

def lock_door():
    global unlock 
    unlock = False  # Đặt trạng thái mở khóa là False
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Khóa cửa và vô hiệu hóa relay
    show_message("Cửa đã bị khóa.")  # Hiển thị thông báo

# Kích hoạt âm thanh đúng
def activate_correct_alarm():
    GPIO.output(ALARM_PIN, GPIO.HIGH)  # Bật còi báo động
    correct_alarm_sound.play()  # Phát âm thanh đúng
    show_message("Âm thanh đúng: Cửa đã được mở.")  # Hiển thị thông báo chỉ báo âm thanh đúng đã được bật

# Kích hoạt âm thanh sai
def activate_incorrect_alarm():
    GPIO.output(ALARM_PIN, GPIO.HIGH)  # Bật còi báo động
    incorrect_alarm_sound.play()  # Phát âm thanh sai
    show_message("Âm thanh sai: Truy cập không hợp lệ!")  # Hiển thị thông báo chỉ báo âm thanh sai đã được bật

# Hàm tắt còi báo động
def deactivate_alarm():
    GPIO.output(ALARM_PIN, GPIO.LOW)  # Tắt còi báo động
    show_message("Cảnh báo: Âm thanh đã được tắt.")  # Hiển thị thông báo chỉ báo âm thanh đã tắt

# Hàm tắt relay
def turn_off_relay():
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Đặt chân relay về LOW

# Hàm làm sạch GPIO
def cleanup():
    GPIO.cleanup()  # Làm sạch trạng thái GPIO

# Hàm quét thẻ
def start_card_scan():
    GPIO.output(SCAN_STATUS_PIN, GPIO.HIGH)  # Bắt đầu quét thẻ
    show_message("Đang quét thẻ...")  # Hiển thị thông báo quét thẻ

def stop_card_scan():
    GPIO.output(SCAN_STATUS_PIN, GPIO.LOW)  # Dừng quét thẻ
    show_message("Kết thúc quét thẻ.")  # Hiển thị thông báo kết thúc quét thẻ

# Lấy trạng thái cửa và thời gian cuối cùng cửa chuyển đổi trạng thái
def get_door_status():
    return door_open  # Trả về trạng thái của cửa

def get_prevTime1():
    return prevTime1  # Trả về thời gian cuối cùng cửa chuyển đổi trạng thái
