from flask import Flask, jsonify, request

app = Flask(__name__)  # Khởi tạo ứng dụng Flask

# Mô phỏng database lưu trữ thông tin RFID
rfid_db = {
    '1234567890': {'name': 'Minh Phuong', 'access': 'unlock'},  # Thông tin người dùng Minh Phuong
    '9876543210': {'name': 'Tung Duong', 'access': 'lock'},     # Thông tin người dùng Tung Duong
    '1111111111': {'name': 'Quang Linh', 'access': 'unlock'}     # Thông tin người dùng Quang Linh
}

# API để kiểm tra thông tin RFID
@app.route('/api/user', methods=['GET'])
def check_rfid():
    """
    Hàm xử lý yêu cầu API GET để kiểm tra thông tin của người dùng qua RFID.
    Lấy tham số 'rfId' từ yêu cầu GET và kiểm tra thông tin trong cơ sở dữ liệu mô phỏng (rfid_db).
    Nếu RFID tồn tại, trả về thông tin người dùng dưới dạng JSON.
    Nếu không tồn tại, trả về thông báo lỗi và mã lỗi 404.
    """
    rfid = request.args.get('rfId')  # Lấy tham số rfId từ yêu cầu GET
    
    # Kiểm tra nếu RFID tồn tại trong database
    if rfid in rfid_db:
        return jsonify(rfid_db[rfid])  # Trả về thông tin người dùng dưới dạng JSON
    else:
        return jsonify({'error': 'RFID not found'}), 404  # Trả về mã lỗi 404 khi không tìm thấy RFID

if __name__ == '__main__':
    app.run(debug=True)  # Chạy ứng dụng Flask với chế độ debug
