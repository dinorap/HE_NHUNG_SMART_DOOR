import tkinter as tk  # Thư viện GUI cho Python
from tkinter import messagebox, simpledialog  # Hộp thoại thông báo và nhập liệu
import os  # Thư viện thao tác với hệ thống tệp
import time  # Thư viện để thao tác với thời gian
from display import DisplayScreen  # Thư viện để hiển thị thông báo

# Khởi tạo màn hình hiển thị
display = DisplayScreen()

# Biến toàn cục
canvas = None  # Biến canvas để vẽ hình
card = None  # Biến để lưu thẻ RFID
card_text = None  # Biến để lưu văn bản hiển thị trên thẻ
label = None  # Biến để lưu nhãn thông báo
card_pos = (450, 130)  # Vị trí ban đầu của thẻ
rfid = None  # Biến cho RFID
card_width = 80  # Giả định mỗi ký tự chiếm khoảng 8 pixel
doorUnlock = False  # Biến xác định trạng thái khóa
prevTime = 0  # Thời gian trước đó
running = True  # Biến toàn cục để điều khiển vòng lặp
rfid_tag = ""  # Biến lưu tên thẻ RFID
rfid_number = ""  # Biến lưu số RFID

def load_rfid(master):
    """Tải RFID từ đầu vào và tạo một thẻ."""
    global rfid_tag, rfid_number  # Khai báo biến toàn cục để cập nhật giá trị

    # Hỏi người dùng tên thẻ và số RFID một lần
    rfid_tag = simpledialog.askstring("Enter Card Name", "Enter card name (without .txt suffix):", parent=master)
    if rfid_tag is None:  # Kiểm tra nếu người dùng nhấn ESC
        return None
    rfid_number = simpledialog.askstring("Enter RFID Number", "Enter RFID number:", parent=master)
    if rfid_number is None:  # Kiểm tra nếu người dùng nhấn ESC
        return None

    if rfid_tag and rfid_number:  # Kiểm tra nếu cả tên thẻ và số RFID đều được cung cấp
        update_card_size(rfid_number)  # Cập nhật kích thước thẻ dựa trên ID
        canvas.itemconfig(card_text, text=rfid_number)  # Hiển thị ID trên thẻ
    else:
        messagebox.showerror("Error", "Please enter a valid card name and RFID number.")  # Thông báo lỗi

def update_card_size(rfid):
    """Cập nhật kích thước thẻ dựa trên ID."""
    global card_width
    text_length = len(rfid)  # Tính chiều dài văn bản
    card_width = text_length * 8  # Giả định mỗi ký tự chiếm khoảng 8 pixel
    canvas.coords(card, 450, 130, 450 + card_width, 170)  # Cập nhật vị trí thẻ
    canvas.coords(card_text, 450 + card_width / 2, 150)  # Cập nhật vị trí văn bản

def start_drag(event):
    """Bắt đầu kéo thẻ."""
    global offset_x, offset_y
    offset_x = event.x - card_pos[0]  # Tính toán độ dịch chuyển theo trục x
    offset_y = event.y - card_pos[1]  # Tính toán độ dịch chuyển theo trục y

def drag(event):
    """Kéo thẻ."""
    global card_pos
    x = event.x - offset_x  # Vị trí mới theo trục x
    y = event.y - offset_y  # Vị trí mới theo trục y

    # Giới hạn vị trí theo biên
    if x < 0:
        x = 0
    elif x > 600 - card_width:  # Giới hạn dựa trên chiều rộng thẻ
        x = 600 - card_width

    # Di chuyển thẻ
    canvas.move(card, x - card_pos[0], 0)
    canvas.move(card_text, x - card_pos[0], 0)
    card_pos = (x, card_pos[1])  # Cập nhật vị trí thẻ

    # Cập nhật nhãn thông báo
    if 100 <= x <= 400 and 100 <= card_pos[1] <= 200:
        canvas.itemconfig(label, text="Card is being scanned!", fill='green')
    else:
        canvas.itemconfig(label, text="Drag the card here", fill='black')

def release(event):
    """Xử lý khi thả thẻ."""
    global doorUnlock, prevTime
    global rfid_tag, rfid_number  # Khai báo thẻ RFID và số là toàn cục
    print(f"Current RFID: {rfid_number}")  # In ra số RFID hiện tại

    # Bắt đầu quét thẻ
    if 100 <= card_pos[0] <= 400 and 100 <= card_pos[1] <= 200:
        prevTime = time.time()  # Lưu thời gian hiện tại
        filename = os.path.join('RFID', rfid_tag + '.txt')  # Tạo đường dẫn cho file
        write_rfid_to_file(filename, rfid_number)  # Ghi số RFID vào file
        display.add_message("Đã thêm thẻ thành công")  # Hiển thị thông báo thêm thẻ thành công
        doorUnlock = True  # Đặt trạng thái khóa mở
        reset_card()  # Đặt lại vị trí thẻ ngay lập tức
        canvas.itemconfig(label, text="Drag the card here", fill='black')  # Cập nhật nhãn thông báo

def reset_card():
    """Đặt lại vị trí thẻ về vị trí ban đầu."""
    global card_pos
    canvas.move(card, 450 - card_pos[0], 0)  # Di chuyển thẻ về vị trí ban đầu
    canvas.move(card_text, 450 - card_pos[0], 0)  # Di chuyển văn bản về vị trí ban đầu
    card_pos = (450, 130)  # Cập nhật vị trí thẻ

def write_rfid_to_file(filename, data):
    """Ghi dữ liệu vào file."""
    with open(filename, 'w') as file:
        file.write(data)  # Ghi dữ liệu vào file
    print(f"Data written to card: {data}")  # In ra thông báo ghi dữ liệu thành công

def wirte_rfid():
    """Hàm chính để mô phỏng đầu vào RFID."""
    global canvas, card, card_text, label

    root = tk.Tk()  # Tạo cửa sổ chính
    root.title("RFID Scanner Simulation")  # Tiêu đề của cửa sổ
    root.geometry("600x300")  # Kích thước cửa sổ

    canvas = tk.Canvas(root, width=600, height=300, bg='lightgrey')  # Tạo canvas
    canvas.pack()

    # Tạo khu vực quét
    canvas.create_rectangle(100, 100, 400, 200, fill='white', outline='black', width=3)
    label = canvas.create_text(250, 150, text="Drag the card here", fill='black', font=("Arial", 12))

    # Tạo thẻ
    card_width = 10 * 8  # Giả định mỗi ký tự chiếm khoảng 8 pixel
    card = canvas.create_rectangle(450, 130, 450 + card_width, 170, fill='blue', outline='black', width=2)
    card_text = canvas.create_text(470 + card_width / 2, 150, text="", fill='white', font=("Arial", 10, "bold"))

    # Gắn sự kiện cho thẻ
    canvas.tag_bind(card, '<Button-1>', start_drag)  # Bắt đầu kéo thẻ
    canvas.tag_bind(card, '<B1-Motion>', drag)  # Kéo thẻ
    canvas.tag_bind(card, '<ButtonRelease-1>', release)  # Thả thẻ

    load_rfid(root)  # Tải đầu vào RFID

    # Gắn phím ESC để thoát về menu chính
    root.bind('<Escape>', lambda event: root.destroy())  # Thoát khi nhấn ESC

    # Vòng lặp chính
    def exit_password_entry(event=None):
        """Hàm thoát khỏi màn hình nhập mật khẩu và quay về menu chính."""
        global running
        running = False  # Đặt biến running thành False để dừng vòng lặp
        display.clear_message()  # Xóa thông báo
        stop_main_loop()  # Dừng tất cả các vòng lặp after

        if root:
            messagebox.showinfo("Thông báo", "Thoát về menu chính.")  # Hiển thị thông báo
            display.clear_message()  # Xóa thông báo
            root.after(100, root.quit)  # Thoát sau 100ms
            root.after(100, root.destroy)  # Đóng cửa sổ hiện tại sau 100ms

    def stop_main_loop():
        """Dừng tất cả các vòng lặp after đang chạy."""
        root.after_cancel(main_loop_after_id)  # Hủy vòng lặp chính

    global main_loop_after_id  # Khai báo biến toàn cục cho ID vòng lặp chính

    def main_loop():
        """Vòng lặp chính để kiểm tra trạng thái nút bấm và khóa tự động."""
        if running:  # Chỉ tiếp tục vòng lặp nếu running là True
            global main_loop_after_id
            main_loop_after_id = root.after(100, main_loop)  # Lưu ID của vòng lặp after

    root.bind('<Escape>', exit_password_entry)  # Gắn phím ESC để thoát
    main_loop()  # Bắt đầu vòng lặp chính
    root.mainloop()  # Bắt đầu vòng lặp GUI
