import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import os
import time
from gpio_setup import *
from display import DisplayScreen
import threading
from send_email import *
display = DisplayScreen()  # Khởi tạo đối tượng DisplayScreen để hiển thị thông báo
# Các biến toàn cục
canvas = None
card = None
card_text = None
label = None
card_pos = (450, 130)  # Vị trí khởi tạo của thẻ
rfid = None  # Biến lưu trữ ID RFID
card_width = 80  # Giả định mỗi ký tự chiếm khoảng 8 pixels
doorUnlock = False  # Biến kiểm soát trạng thái mở khóa cửa
prevTime = 0  # Biến lưu thời gian trước đó
running = True  # Biến toàn cục để kiểm soát vòng lặp
count = 0
def load_rfid(master):
    """Tải RFID từ file và hiển thị trên thẻ."""
    global rfid  # Khai báo biến rfid là global để cập nhật giá trị
    
    def exit_to_menu(event=None):
        """Thoát về menu chính khi nhấn ESC."""
        messagebox.showinfo("Thông báo", "Thoát về menu chính.")
        master.after(100, master.quit)  # Thoát sau 100ms
        master.after(100, master.destroy)  # Đóng cửa sổ hiện tại sau 100ms
        

    # Gán phím ESC để thoát về menu chính
    master.bind('<Escape>', exit_to_menu)

    while True:  # Vòng lặp để cho phép người dùng nhập lại mã thẻ
        rfid_tag = simpledialog.askstring("Nhập tên thẻ", "Nhập tên thẻ (không có đuôi .txt) hoặc ấn 'q' để thoát:", parent=master)

        if rfid_tag == 'q':  # Thoát nếu người dùng nhập 'q'
            exit_to_menu()  # Gọi hàm thoát về menu chính
            return None

        if rfid_tag:  # Kiểm tra nếu người dùng nhập dữ liệu
            filename = os.path.join('RFID', rfid_tag + '.txt')  # Tạo đường dẫn tới file chứa RFID
            rfid = read_rfid_from_file(filename)  # Đọc số RFID từ file

            if rfid:  # Nếu đọc thẻ thành công
                update_card_size(rfid)  # Cập nhật kích thước thẻ dựa trên ID
                canvas.itemconfig(card_text, text=rfid)  # Hiển thị ID trên thẻ
                return rfid  # Kết thúc vòng lặp và trả về mã thẻ
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy thẻ RFID. Vui lòng thử lại.")
        elif rfid_tag is None:
            # Không hiển thị lỗi nếu người dùng nhấn ESC để thoát
            return None
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên thẻ hợp lệ.")

def update_card_size(rfid):
    """Cập nhật kích thước thẻ dựa trên ID."""
    global card_width
    text_length = len(rfid)  # Đo độ dài của ID RFID
    card_width = text_length * 8  # Giả định mỗi ký tự chiếm khoảng 8 pixels
    # Cập nhật vị trí thẻ và văn bản dựa trên kích thước mới
    canvas.coords(card, 450, 130, 450 + card_width, 170)  
    canvas.coords(card_text, 450 + card_width / 2, 150)  # Cập nhật vị trí văn bản

def start_drag(event):
    """Khởi động kéo thẻ."""
    global offset_x, offset_y
    offset_x = event.x - card_pos[0]  # Tính toán độ lệch x
    offset_y = event.y - card_pos[1]  # Tính toán độ lệch y

def drag(event):
    """Kéo thẻ."""
    global card_pos
    x = event.x - offset_x
    y = event.y - offset_y

    # Giới hạn vị trí kéo thẻ
    if x < 0:
        x = 0
    elif x > 600 - card_width:  # Giới hạn theo chiều rộng của thẻ
        x = 600 - card_width

    # Kéo thẻ
    canvas.move(card, x - card_pos[0], 0)
    canvas.move(card_text, x - card_pos[0], 0)
    card_pos = (x, card_pos[1])  # Cập nhật vị trí thẻ

    # Hiển thị trạng thái kéo thẻ
    if 100 <= x <= 400 and 100 <= card_pos[1] <= 200:
        canvas.itemconfig(label, text="Thẻ đã quét!", fill='green')
    else:
        canvas.itemconfig(label, text="Kéo thẻ vào đây", fill='black')

def release(event):
    """Xử lý khi thả thẻ."""
    global rfid  # Khai báo biến rfid là global
    print(f"RFID hiện tại: {rfid}")

    # Bắt đầu quét thẻ
    start_card_scan()

    if 100 <= card_pos[0] <= 400 and 100 <= card_pos[1] <= 200:
        user_info = send_to_api(rfid)  # Gửi RFID tới API
        if user_info:
            activate_correct_alarm()
            threading.Timer(3.0, deactivate_alarm).start()
            # Hiển thị thông tin người dùng
            messagebox.showinfo("Thông báo", f"Thẻ đã được quét thành công!\nTên người dùng: {user_info['name']}\nTrạng thái truy cập: {user_info['access']}")
            unlock_door()  # Mở khóa cửa
            prevTime = time.time() 
            doorUnlock = True  # Đánh dấu cửa đã mở
            reset_card()  # Đặt lại vị trí của thẻ ngay lập tức
            canvas.itemconfig(label, text="Kéo thẻ vào đây", fill='black')
    # Dừng quét thẻ
    stop_card_scan()

def reset_card():
    """Đặt lại vị trí của thẻ về ban đầu."""
    global card_pos
    canvas.move(card, 450 - card_pos[0], 0)  # Di chuyển thẻ về vị trí 450
    canvas.move(card_text, 450 - card_pos[0], 0)  # Di chuyển văn bản về vị trí tương ứng
    card_pos = (450, 130)  # Cập nhật vị trí thẻ về ban đầu

def read_rfid_from_file(filename):
    """Đọc dữ liệu từ file."""
    try:
        with open(filename, 'r') as file:
            rfid_data = file.read().strip()  # Đọc dữ liệu từ file và loại bỏ khoảng trắng
        print(f"Đã đọc dữ liệu từ thẻ với ID: {rfid_data}")
        return rfid_data  # Trả về dữ liệu RFID
    except FileNotFoundError:
        return None  # Nếu file không tìm thấy, trả về None

def send_to_api(rfid):
    """Gửi số RFID tới API và nhận kết quả."""
    API_URL = 'http://127.0.0.1:5000/api/user'
    global count 
    try:
        response = requests.get(API_URL, params={'rfId': rfid})  # Gửi yêu cầu GET tới API với số RFID
        data = response.json()  # Chuyển đổi phản hồi thành định dạng JSON

        print(f"Dữ liệu trả về từ API: {data}")  # Thêm dòng này để kiểm tra dữ liệu trả về
        
        if 'error' in data:  # Kiểm tra nếu có lỗi trong dữ liệu trả về
            count +=1
            activate_incorrect_alarm()
            threading.Timer(3.0, deactivate_alarm).start()
            messagebox.showerror("Lỗi", "Thẻ RFID không hợp lệ!")  # Hiển thị thông báo lỗi
            if count >= 3:
                SendEmail()  # Gọi hàm gửi email
                messagebox.showwarning("Cảnh báo", "Đã nhập sai mật khẩu quá 3 lần! Đã gửi email cảnh báo.")
                count = 0
            reset_card()  # Đặt lại vị trí của thẻ ngay lập tức
            canvas.itemconfig(label, text="Kéo thẻ vào đây", fill='black')
            return None
        elif 'name' in data and 'access' in data:  # Kiểm tra dữ liệu hợp lệ
            # Kiểm tra nếu quyền truy cập là 'lock'
            if data['access'] == 'lock':
                count +=1
                activate_incorrect_alarm()
                threading.Timer(3.0, deactivate_alarm).start()
                messagebox.showwarning("Thẻ bị khóa", f"Thẻ của bạn ({data['name']}) đã bị khóa. Không thể mở cửa.")
                if count >= 3:
                    SendEmail()  # Gọi hàm gửi email
                    messagebox.showwarning("Cảnh báo", "Đã nhập sai mật khẩu quá 3 lần! Đã gửi email cảnh báo.")
                    count = 0
                reset_card()  # Đặt lại vị trí thẻ ngay lập tức
                canvas.itemconfig(label, text="Kéo thẻ vào đây", fill='black')
                return None
            else:
                return data  # Trả về dữ liệu nếu quyền truy cập không bị khóa
        else:
            messagebox.showerror("Lỗi dữ liệu", "Dữ liệu trả về từ API không hợp lệ.")
            return None
    except requests.exceptions.RequestException as e:  # Xử lý lỗi kết nối
        messagebox.showerror("Lỗi kết nối", "Không thể kết nối tới API.")
        return None

def simulate_rfid_input():
    """Hàm chính để mô phỏng đầu vào RFID."""
    global canvas, card, card_text, label

    root = tk.Tk()  # Tạo cửa sổ chính
    root.title("RFID Scanner Simulation")  # Tiêu đề cửa sổ
    root.geometry("600x300")  # Kích thước cửa sổ

    canvas = tk.Canvas(root, width=600, height=300, bg='lightgrey')  # Tạo canvas để vẽ
    canvas.pack()

    # Tạo ô quét thẻ
    canvas.create_rectangle(100, 100, 400, 200, fill='white', outline='black', width=3)
    label = canvas.create_text(250, 150, text="Kéo thẻ vào đây", fill='black', font=("Arial", 12))  # Nhãn hướng dẫn

    # Tạo thẻ
    card_width = 10 * 8  # Giả định mỗi ký tự chiếm khoảng 8 pixels
    card = canvas.create_rectangle(450, 130, 450 + card_width, 170, fill='blue', outline='black', width=2)  # Tạo hình chữ nhật cho thẻ
    card_text = canvas.create_text(470 + card_width / 2, 150, text="", fill='white', font=("Arial", 10, "bold"))  # Tạo văn bản trên thẻ

    # Gán các sự kiện kéo cho thẻ
    canvas.tag_bind(card, '<Button-1>', start_drag)  # Bắt đầu kéo thẻ khi nhấn chuột
    canvas.tag_bind(card, '<B1-Motion>', drag)  # Kéo thẻ khi di chuyển chuột
    canvas.tag_bind(card, '<ButtonRelease-1>', release)  # Xử lý khi thả thẻ

    load_rfid(root)  # Gọi hàm để tải RFID

    # Gán phím ESC để thoát về menu chính
    root.bind('<Escape>', lambda event: root.destroy())

    def auto_lock_door():
        """Hàm tự động khóa cửa sau 15 giây nếu nó đã được mở."""
        global doorUnlock, prevTime

        # Kiểm tra trạng thái cửa
        if get_door_status() == False:
            # Nếu cửa đang mở
            if get_prevTime1() > prevTime:
                prevTime = get_prevTime1()

            # Nếu cửa đã mở hơn 15 giây, tự động khóa
            if doorUnlock and (time.time() - prevTime > 15):
                doorUnlock = False
                lock_door()  # Gọi hàm để khóa cửa
                show_message("Door locked")  # Hiện thông báo khóa cửa
    
    def exit_password_entry(event=None):
        """Hàm thoát khỏi màn hình nhập mật khẩu và quay về menu chính."""
        global running
        running = False  # Đặt biến running thành False để dừng vòng lặp
        display.clear_message()  # Xóa thông điệp trên màn hình
        stop_main_loop()  # Dừng tất cả các vòng lặp after
        turn_off_relay()  # Tắt relay

        if root:
            messagebox.showinfo("Thông báo", "Thoát về menu chính.")
            display.clear_message()  # Xóa thông điệp
            root.after(100, root.quit)  # Thoát sau 100ms
            root.after(100, root.destroy)  # Đóng cửa sổ hiện tại sau 100ms

    def stop_main_loop():
        """Dừng tất cả các vòng lặp after đang chạy."""
        root.after_cancel(main_loop_after_id)  # Hủy vòng lặp chính

    global main_loop_after_id
    def main_loop():
        """Vòng lặp chính để kiểm tra trạng thái nút bấm và khóa tự động."""
        if running:  # Chỉ tiếp tục vòng lặp nếu running là True
            check_button()  # Kiểm tra trạng thái nút bấm
            auto_lock_door()  # Kiểm tra khóa tự động
            global main_loop_after_id
            main_loop_after_id = root.after(100, main_loop)  # Lưu ID của vòng lặp after
        
    root.bind('<Escape>', exit_password_entry)  # Gán phím ESC để thoát
    main_loop()  # Bắt đầu vòng lặp chính
    root.mainloop()  # Bắt đầu vòng lặp chính của Tkinter
