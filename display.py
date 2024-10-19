import pygame

class DisplayScreen:
    def __init__(self, width=500, height=200):
        # Khởi tạo Pygame và thiết lập màn hình
        pygame.init()  # Khởi động Pygame
        self.width = width  # Chiều rộng của màn hình
        self.height = height  # Chiều cao của màn hình
        self.screen = pygame.display.set_mode((self.width, self.height))  # Thiết lập kích thước cửa sổ Pygame
        pygame.display.set_caption("Display Screen")  # Đặt tiêu đề cửa sổ
        
        # Thay đổi font để hỗ trợ tiếng Việt
        self.font = pygame.font.Font("Font/font-times-new-roman.ttf", 24)  # Đường dẫn đến tệp font chữ
        self.lines = []  # Danh sách các dòng để hiển thị
        self.bg_color = (0, 0, 0)  # Màu nền (đen)
        self.text_color = (0, 255, 0)  # Màu chữ (xanh lá cây)

    def add_message(self, message):
        """Thêm một dòng thông báo mới lên màn hình. Nếu có quá 5 dòng, dòng cũ nhất sẽ bị xóa."""
        if len(self.lines) >= 5:  # Giới hạn hiển thị tối đa 5 dòng
            self.lines.pop(0)  # Xóa dòng cũ nhất
        self.lines.append(message)  # Thêm dòng mới vào danh sách
        self.display()  # Hiển thị dòng thông báo mới

    def clear(self):
        """Xóa toàn bộ các dòng thông báo khỏi màn hình."""
        self.lines = []  # Xóa danh sách các dòng
        self.display()  # Làm mới màn hình để hiển thị thay đổi

    def display(self):
        """Hiển thị các dòng thông báo lên màn hình."""
        self.screen.fill(self.bg_color)  # Xóa toàn bộ màn hình với màu nền
        for i, line in enumerate(self.lines):  # Lặp qua từng dòng
            rendered_text = self.font.render(line, True, self.text_color)  # Tạo đối tượng văn bản từ dòng thông báo
            self.screen.blit(rendered_text, (10, i * 30 + 10))  # Vẽ dòng lên màn hình tại vị trí nhất định
        pygame.display.flip()  # Cập nhật toàn bộ màn hình với nội dung mới

    def clear_message(self):
        """Xóa tất cả các thông báo hiển thị trên màn hình."""
        self.lines = []  # Xóa toàn bộ thông báo
        self.display()  # Cập nhật lại màn hình để hiển thị sự thay đổi

    def close(self):
        """Đóng ứng dụng Pygame."""
        pygame.quit()  # Thoát khỏi Pygame

# Ví dụ sử dụng
display = DisplayScreen()  # Khởi tạo đối tượng DisplayScreen

def show_message(message):
    """Thêm thông báo để hiển thị trên màn hình."""
    display.add_message(message)  # Gọi hàm thêm thông báo từ đối tượng DisplayScreen

def clear_message():
    """Xóa tất cả các thông báo trên màn hình."""
    display.clear_message()  # Gọi hàm xóa thông báo từ đối tượng DisplayScreen
