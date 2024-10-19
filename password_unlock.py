import tkinter as tk 
from tkinter import messagebox
from gpio_setup import *
from display import DisplayScreen  # Import class DisplayScreen từ file bạn đã tạo

prevTime = 0
doorUnlock = False
running = True  # Biến toàn cục để kiểm soát vòng lặp

def password_entry_system():
    """Hàm khởi tạo hệ thống nhập mật khẩu và giao diện người dùng."""

    # Khởi tạo màn hình Pygame để hiển thị mật khẩu
    display = DisplayScreen()

    correct_password = "123456"  # Mật khẩu đúng
    entered_password = ""  # Mật khẩu đã nhập

    def show_message(message):
        """Hàm hiển thị duy nhất 1 dòng trên màn hình Pygame"""
        display.clear()  # Xóa nội dung cũ trên màn hình
        display.add_message(message)  # Thêm dòng thông báo mới

    def add_digit(digit):
        """Hàm xử lý khi người dùng nhấn vào nút số."""
        nonlocal entered_password
        entered_password += str(digit)  # Thêm chữ số vào mật khẩu đã nhập
        password_var.set('*' * len(entered_password))  # Hiển thị mật khẩu với dấu *

        # Cập nhật hiển thị lên màn hình Pygame với nội dung mới
        show_message(f"Nhập mật khẩu : {'*' * len(entered_password)}")

    def clear_password():
        """Xóa toàn bộ mật khẩu đã nhập."""
        nonlocal entered_password
        entered_password = ""
        password_var.set("")
        show_message(f"Nhập mật khẩu : ")
    def clear_password1():
        """Xóa toàn bộ mật khẩu đã nhập."""
        nonlocal entered_password
        entered_password = ""
        password_var.set("")

    def check_password():
        """Kiểm tra mật khẩu và mở khóa nếu đúng."""
        global doorUnlock, prevTime
        if doorUnlock:
            check_u()
            clear_password1()
            return  # Nếu cửa đang mở khóa, không cho phép nhập mật khẩu
        if len(entered_password) >= 6 and entered_password[-6:] == correct_password:
            # show_message("Password correct. Door unlocked!")
            unlock_door()
            activate_correct_alarm()
            root.after(3000,lambda: deactivate_alarm())
            doorUnlock = True
            prevTime = time.time()
            print(prevTime)
            clear_password1()  # Xóa mật khẩu đã nhập
        else:
            clear_password()
            activate_incorrect_alarm()
            root.after(2000,lambda: deactivate_alarm())
            show_message("Mật khẩu sai vui lòng nhập lại.")
            root.after(3000,lambda: clear_password())
            

    def auto_lock_door():
        """Hàm tự động khóa cửa sau 15 giây nếu nó đã được mở."""
        global doorUnlock, prevTime

        # Kiểm tra trạng thái cửa
        if get_door_status() == False:
            # Nếu cửa đang mở
            if get_prevTime1() > prevTime:
                prevTime = get_prevTime1()

            # Nếu cửa đã mở hơn 5 giây, tự động khóa
            if doorUnlock and (time.time() - prevTime > 5):
                doorUnlock = False
                lock_door()  # Gọi hàm để khóa cửa
                root.after(2000, lambda: show_message("Nhập mật khẩu :"))

    def create_number_pad(root):
        """Tạo bàn phím số trên giao diện."""
        buttons_frame = tk.Frame(root)
        buttons_frame.pack()

        # Các số từ 1 đến 9
        digits = [
            ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
            ('0', 4, 1)
        ]

        for (digit, row, col) in digits:
            btn = tk.Button(buttons_frame, text=digit, width=5, height=2, command=lambda d=digit: add_digit(d))
            btn.grid(row=row, column=col)

        # Nút 'Clear' để xóa mật khẩu
        clear_button = tk.Button(buttons_frame, text='Clear', width=5, height=2, command=clear_password)
        clear_button.grid(row=4, column=0)

        # Nút 'Enter' để xác nhận mật khẩu
        enter_button = tk.Button(buttons_frame, text='Enter', width=5, height=2, command=check_password)
        enter_button.grid(row=4, column=2)

    def exit_password_entry(event=None):
        """Hàm thoát khỏi màn hình nhập mật khẩu và quay về menu chính."""
        global running
        running = False  # Đặt biến running thành False để dừng vòng lặp
        display.clear_message()
        stop_main_loop()  # Dừng tất cả các vòng lặp after
        turn_off_relay()

        if root:
            messagebox.showinfo("Thông báo", "Thoát về menu chính.")
            display.clear_message()
            root.after(100, root.quit)  # Thoát sau 100ms
            root.after(100, root.destroy)  # Đóng cửa sổ hiện tại sau 100ms

           

    def stop_main_loop():
        """Dừng tất cả các vòng lặp after đang chạy."""
        root.after_cancel(main_loop_after_id)  # Hủy vòng lặp chính

    # Tạo giao diện chính
    global root
    root = tk.Tk()
    root.title("Password Entry System")
    root.geometry("200x250")
    
    # Biến lưu trữ mật khẩu nhập vào và màn hình hiển thị
    password_var = tk.StringVar()
    password_label = tk.Label(root, textvariable=password_var, font=("Arial", 24), width=12, anchor='e')
    password_label.pack(pady=10)

    # Hiển thị thông báo "Nhập mật khẩu :" ngay khi hệ thống khởi động
    show_message("Nhập mật khẩu :")

    global main_loop_after_id
    def main_loop():
        """Vòng lặp chính để kiểm tra trạng thái nút bấm và khóa tự động."""
        if running:  # Chỉ tiếp tục vòng lặp nếu running là True
            check_button()  # Kiểm tra trạng thái nút bấm
            auto_lock_door()
            global main_loop_after_id
            main_loop_after_id = root.after(100, main_loop)  # Lưu ID của vòng lặp after

    # Tạo bàn phím số
    create_number_pad(root)
    main_loop()

    # Gán sự kiện cho phím Esc
    root.bind("<Escape>", exit_password_entry)

    # Bắt đầu vòng lặp của tkinter
    root.mainloop()
