import tkinter as tk
from tkinter import messagebox
import subprocess
from display import DisplayScreen
from gpio_setup import *
from face_auto_shot import capture_and_train

def admin_password():
    """
    Hàm xử lý việc nhập mật khẩu của quản trị viên.
    Tạo giao diện người dùng cho việc nhập mật khẩu và tên người dùng.
    """
    display = DisplayScreen()  # Tạo đối tượng màn hình hiển thị
    correct_admin_password = "123456"  # Mật khẩu admin đúng
    entered_password = ""  # Mật khẩu người dùng đã nhập
    username = ""  # Tên người dùng đã nhập

    def show_message(message):
        """Hàm hiển thị duy nhất 1 dòng trên màn hình Pygame."""
        display.clear()  # Xóa nội dung cũ trên màn hình
        display.add_message(message)  # Thêm dòng thông báo mới

    def add_digit(digit):
        """Thêm một chữ số vào mật khẩu đã nhập."""
        nonlocal entered_password
        entered_password += str(digit)  # Thêm chữ số vào mật khẩu
        password_var.set('*' * len(entered_password))  # Hiển thị dấu sao thay cho mật khẩu thực
        show_message(f"Nhập mật khẩu : {'*' * len(entered_password)}")  # Hiển thị thông báo mật khẩu

    def clear_password():
        """Xóa mật khẩu đã nhập."""
        nonlocal entered_password
        entered_password = ""  # Xóa mật khẩu
        password_var.set("")  # Xóa hiển thị mật khẩu
        show_message(f"Nhập mật khẩu : ")  # Hiển thị thông báo nhập lại mật khẩu

    def check_password():
        """Kiểm tra mật khẩu đã nhập."""
        if len(entered_password) >= 6 and entered_password[-6:] == correct_admin_password:
            show_message("Mật khẩu đúng.")  # Hiển thị thông báo mật khẩu đúng
            password_frame.pack_forget()  # Ẩn khung nhập mật khẩu
            create_username_entry()  # Tạo khung nhập tên người dùng
        else:
            clear_password()  # Xóa mật khẩu nếu sai
            show_message("Sai mật khẩu. Vui lòng thử lại.")  # Hiển thị thông báo mật khẩu sai

    def create_number_pad():
        """Tạo bàn phím số."""
        global password_frame  # Khai báo biến toàn cục để thay đổi hiển thị
        password_frame = tk.Frame(password_window)  # Khung cho bàn phím số
        password_frame.pack()

        buttons_frame = tk.Frame(password_frame)  # Khung chứa các nút bấm
        buttons_frame.pack()

        # Các nút số từ 1 đến 9 và 0
        digits = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]

        for (digit, row, col) in digits:
            btn = tk.Button(buttons_frame, text=digit, width=5, height=2, command=lambda d=digit: add_digit(d))  # Tạo nút số
            btn.grid(row=row, column=col)  # Đặt vị trí nút

        # Nút Clear để xóa mật khẩu đã nhập
        clear_button = tk.Button(buttons_frame, text='Clear', width=5, height=2, command=clear_password)
        clear_button.grid(row=3, column=0)  # Vị trí nút Clear

        # Nút Enter để kiểm tra mật khẩu
        enter_button = tk.Button(buttons_frame, text='Enter', width=5, height=2, command=check_password)
        enter_button.grid(row=3, column=2)  # Vị trí nút Enter

    def create_username_entry():
        """Tạo khung nhập tên người dùng sau khi mật khẩu đúng."""
        username_label = tk.Label(password_window, text="Nhập tên người dùng:", font=("Arial", 12))
        username_label.pack(pady=5)  # Nhãn hiển thị yêu cầu nhập tên người dùng

        username_entry = tk.Entry(password_window, font=("Arial", 12))
        username_entry.pack(pady=5)  # Ô nhập tên người dùng

        def get_username():
            """Lấy tên người dùng đã nhập và gọi hàm nhận diện khuôn mặt."""
            nonlocal username
            username = username_entry.get()  # Lấy tên người dùng đã nhập
            password_window.destroy()  # Đóng cửa sổ sau khi nhập thành công
            capture_and_train(username)  # Gọi script nhận diện khuôn mặt với tên người dùng đã nhập
            display.clear_message()  # Xóa thông báo hiển thị
            password_window.quit()  # Thoát vòng lặp Tkinter

        # Nút Submit để xác nhận tên người dùng
        submit_button = tk.Button(password_window, text="Submit", command=get_username)
        submit_button.pack(pady=5)  # Nút Submit

    def exit_password_entry(event=None):
        """Hàm thoát khỏi màn hình nhập mật khẩu và quay về menu chính."""
        global running
        running = False  # Đặt biến running thành False để dừng vòng lặp
        display.clear_message()  # Xóa thông báo hiển thị

        if password_window:
            messagebox.showinfo("Thông báo", "Thoát về menu chính.")  # Hiển thị thông báo thoát về menu chính
            display.clear_message()  # Xóa thông báo hiển thị
            password_window.after(100, password_window.quit)  # Thoát sau 100ms
            password_window.after(100, password_window.destroy)  # Đóng cửa sổ hiện tại sau 100ms

    # Tạo cửa sổ chính để nhập mật khẩu
    password_window = tk.Tk()
    password_window.title("Nhập mật khẩu admin")  # Tiêu đề cửa sổ
    password_window.geometry("250x350")  # Kích thước cửa sổ

    # Gán phím ESC để thoát về menu
    password_window.bind("<Escape>", exit_password_entry)

    # Biến lưu mật khẩu đã nhập
    password_var = tk.StringVar()
    password_label = tk.Label(password_window, textvariable=password_var, font=("Arial", 24), width=12, anchor='e')  # Nhãn hiển thị mật khẩu
    password_label.pack(pady=10)

    create_number_pad()  # Tạo bàn phím số

    # Hiển thị thông báo ban đầu
    show_message("Nhập mật khẩu:")
    # Bắt đầu vòng lặp chính của Tkinter
    password_window.mainloop()
