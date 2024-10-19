import tkinter as tk  # Thư viện GUI cho Python
from tkinter import messagebox  # Hộp thoại thông báo
from face_recognition import load_known_faces, unlock_with_face  # Thư viện nhận diện khuôn mặt
from password_unlock import password_entry_system  # Thư viện mở khóa bằng mật khẩu
from rfid_simulation import simulate_rfid_input  # Thư viện mô phỏng đầu vào RFID
from admin_functions import admin_password  # Thư viện chức năng quản trị
from wirte_rfid import wirte_rfid  # Thư viện để thêm thẻ RFID
from gpio_setup import gpio_setup, cleanup  # Thư viện để thiết lập GPIO
from display import DisplayScreen  # Thư viện để hiển thị thông báo
import sys  # Thư viện để quản lý hệ thống
import os
from gpio_setup import *

# Khởi tạo màn hình hiển thị
display = DisplayScreen()

class LockSystemApp:
    def __init__(self, master):
        """Khởi tạo ứng dụng khóa."""
        self.master = master  # Cửa sổ chính
        self.master.title("Lock System")  # Tiêu đề của cửa sổ
        self.master.geometry("300x300")  # Kích thước cửa sổ
        self.idle_time_limit = 5000  # Thời gian tối đa không hoạt động (45 giây)
        self.idle_event = None  # Biến để lưu sự kiện hẹn giờ
        self.check()
        # Tạo các widget trong menu chính
        self.create_widgets()
        self.reset_idle_timer()  # Bắt đầu hẹn giờ không hoạt động
        show_message("Xin chào hãy chọn phương thức mở khóa")

    def check(self):
        """Periodically check if the button is pressed to unlock/lock the door."""
        button_unlock()  # Call the button_unlock function to check the button state
        self.master.after(100, self.check)  # Check the button every 100ms

    def reset_idle_timer(self):
        """Reset hẹn giờ không hoạt động."""
        if self.idle_event:
            self.master.after_cancel(self.idle_event)  # Hủy hẹn giờ trước đó
        self.idle_event = self.master.after(self.idle_time_limit, self.auto_exit)  # Thiết lập hẹn giờ mới

    def stop_idle_timer(self):
        """Dừng bộ đếm thời gian không hoạt động."""
        if self.idle_event:
            self.master.after_cancel(self.idle_event)  # Hủy bộ đếm

    def create_widgets(self):
        """Tạo các nút trong menu chính."""
        self.label = tk.Label(self.master, text="Chọn phương thức mở khóa:", font=("Arial", 14))  # Nhãn hướng dẫn
        self.label.pack(pady=10)

        # Nút mở khóa bằng khuôn mặt
        self.face_button = tk.Button(self.master, text="Mở khóa bằng khuôn mặt", command=self.unlock_with_face, width=30)
        self.face_button.pack(pady=5)

        # Nút mở khóa bằng mật khẩu
        self.password_button = tk.Button(self.master, text="Mở khóa bằng mật khẩu", command=self.password_entry_system, width=30)
        self.password_button.pack(pady=5)

        # Nút mô phỏng đầu vào RFID
        self.rfid_button = tk.Button(self.master, text="Mô phỏng đầu vào RFID", command=self.simulate_rfid_input, width=30)
        self.rfid_button.pack(pady=5)

        # Nút thêm khuôn mặt (Admin)
        self.admin_button = tk.Button(self.master, text="Thêm khuôn mặt (Admin)", command=self.admin_password, width=30)
        self.admin_button.pack(pady=5)
        
        # Nút thêm thẻ RFID (Admin)
        self.admin_button = tk.Button(self.master, text="Thêm thẻ RFID (Admin)", command=self.wirte_rfid, width=30)
        self.admin_button.pack(pady=5)

        # Nút thoát
        self.exit_button = tk.Button(self.master, text="Thoát", command=self.exit_program, width=30)
        self.exit_button.pack(pady=5)

    def unlock_with_face(self):
        """Mở khóa bằng nhận diện khuôn mặt."""
        self.stop_idle_timer()  # Dừng hẹn giờ không hoạt động
        self.hide_menu()  # Ẩn cửa sổ chính
        data = load_known_faces()  # Tải các khuôn mặt đã biết
        unlock_with_face(data)  # Thực hiện mở khóa
        self.show_menu()  # Hiển thị lại menu
        self.reset_idle_timer()  # Reset hẹn giờ không hoạt động

    def password_entry_system(self):
        """Gọi hệ thống nhập mật khẩu."""
        self.stop_idle_timer()  # Dừng hẹn giờ không hoạt động
        self.hide_menu()  # Ẩn cửa sổ chính
        password_entry_system()  # Gọi hàm nhập mật khẩu
        self.show_menu()  # Hiển thị lại menu
        self.reset_idle_timer()  # Reset hẹn giờ không hoạt động

    def simulate_rfid_input(self):
        """Mô phỏng đầu vào RFID."""
        self.stop_idle_timer()  # Dừng hẹn giờ không hoạt động
        self.hide_menu()  # Ẩn cửa sổ chính
        simulate_rfid_input()  # Gọi hàm mô phỏng RFID
        self.show_menu()  # Hiển thị lại menu
        self.reset_idle_timer()  # Reset hẹn giờ không hoạt động

    def admin_password(self):
        """Chạy chức năng mật khẩu admin."""
        self.stop_idle_timer()  # Dừng hẹn giờ không hoạt động
        self.hide_menu()  # Ẩn cửa sổ chính
        admin_password()  # Gọi hàm quản lý admin
        self.show_menu()  # Hiển thị lại menu
        self.reset_idle_timer()  # Reset hẹn giờ không hoạt động

    def wirte_rfid(self):
        """Chạy chức năng thêm thẻ RFID."""
        self.stop_idle_timer()  # Dừng hẹn giờ không hoạt động
        self.hide_menu()  # Ẩn cửa sổ chính
        wirte_rfid()  # Gọi hàm thêm thẻ RFID
        self.show_menu()  # Hiển thị lại menu
        self.reset_idle_timer()  # Reset hẹn giờ không hoạt động

    def hide_menu(self):
        """Ẩn menu chính và xóa thông báo."""
        self.master.withdraw()  # Ẩn toàn bộ cửa sổ
        display.clear_message()  # Xóa thông báo trên màn hình

    def show_menu(self):
        """Hiện lại menu chính."""
        self.master.deiconify()  # Hiện cửa sổ lại

    def auto_exit(self):
        """Thoát chương trình một cách an toàn."""
        cleanup()  # Dọn dẹp GPIO
        self.master.quit()  # Thoát vòng lặp chính
        self.master.destroy()  # Đóng cửa sổ Tkinter
        os._exit(0)  # Thoát hệ thống mà không dọn dẹp

    def exit_program(self):
        """Thoát chương trình một cách an toàn."""
        if messagebox.askyesno("Xác nhận thoát", "Bạn có chắc chắn muốn thoát?"):
            cleanup()  # Dọn dẹp GPIO
            self.master.quit()  # Thoát vòng lặp chính
            self.master.destroy()  # Đóng cửa sổ Tkinter
            sys.exit()  # Thoát hệ thống

if __name__ == "__main__":
    gpio_setup()  # Thiết lập GPIO

    root = tk.Tk()  # Tạo cửa sổ chính
    app = LockSystemApp(root)  # Khởi tạo ứng dụng khóa
    root.protocol("WM_DELETE_WINDOW", app.exit_program)  # Đảm bảo dọn dẹp khi đóng cửa sổ
    root.mainloop()  # Bắt đầu vòng lặp GUI
