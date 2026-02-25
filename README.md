# Vehicle Speed Detection

Ứng dụng web phát hiện và theo dõi tốc độ xe cộ trong video sử dụng AI (YOLO + Deep Sort).

## 🎯 Tính năng

- **Phát hiện kendaraan**: Sử dụng YOLO để phát hiện xe trên đường
- **Theo dõi realtime**: Sử dụng Deep Sort tracker để theo dõi các xe qua các frame
- **Tính toán tốc độ**: Tính tốc độ xe dựa trên displacement giữa các frame
- **Giao diện web**: Upload video và xem kết quả trực tiếp trên trình duyệt
- **Flash effect**: Hiệu ứng nhấp nháy khi có xe vượt quá tốc độ quy định

## 📋 Yêu cầu

- Python 3.8+
- Flask
- OpenCV (cv2)
- NumPy
- Ultralytics YOLO
- Deep Sort Realtime
- cvzone
- Werkzeug

## 🚀 Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/nency2277/Vehicle_Speed.git
cd Vehicle_Speed
```

### 2. Tạo virtual environment (tùy chọn nhưng khuyên dùng)
```bash
python -m venv venv
# Trên Windows
venv\Scripts\activate
# Trên Mac/Linux
source venv/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Tải model YOLO
- File `best.pt` đã có trong repository
- Nếu cần model khác, hãy cập nhật đường dẫn trong `app.py`

## 📝 Cấu hình

### Cập nhật đường dẫn model (nếu cần)
Trong `app.py`, dòng 27:
```python
model = YOLO(r"C:\Users\Admin\Desktop\okDATN2025\best.pt")
```

Thay bằng đường dẫn của bạn hoặc:
```python
model = YOLO("best.pt")  # Sử dụng file trong cùng thư mục
```

### Tùy chỉnh
- `line_y1`, `line_y2`: Vị trí các đường thẳng phát hiện tốc độ (dòng 36-37)
- `pixels_per_meter`: Số pixel = 1 mét (dòng 39)
- `line_color_default`, `line_color_triggered`: Màu sắc của đường thẳng (dòng 35)

## 🎬 Sử dụng

### Chạy ứng dụng
```bash
python app.py
```

### Truy cập web interface
- Mở trình duyệt, truy cập: `http://localhost:5000`
- Upload file video
- Xem quá trình phát hiện và tính toán tốc độ realtime

## 📂 Cấu trúc thư mục

```
Vehicle_Speed/
├── app.py                 # Flask application chính
├── best.pt               # YOLO model
├── README.md             # File này
├── requirements.txt      # Danh sách dependencies
├── templates/
│   └── index.html        # Giao diện web
└── uploads/              # Thư mục lưu video upload
```

## 🔧 Troubleshooting

### Lỗi không tìm thấy model
- Kiểm tra đường dẫn file `best.pt` trong `app.py`
- Đảm bảo file model tồn tại trong thư mục dự án

### Ứng dụng chạy chậm
- Giảm kích thước video đầu vào
- Tăng `line_y2 - line_y1` để tăng vùng phát hiện
- Sử dụng GPU nếu có sẵn

### Lỗi CUDA
- Nếu có GPU NVIDIA, cần cài `torch` với CUDA support
- Hoặc để mặc định, ứng dụng sẽ sử dụng CPU

## 📊 Output

Sau khi xử lý, ứng dụng sẽ:
- Hiển thị video với bounding box và ID của các xe
- Hiển thị tốc độ của mỗi xe
- Đánh dấu đỏ (flash) nếu xe vượt quá tốc độ quy định

## 📧 Liên hệ

- Tác giả: NenCy
- GitHub: https://github.com/nency2277

## 📄 License

MIT License - xem file LICENSE để chi tiết

## 🙏 Acknowledgments

- Ultralytics YOLO: https://github.com/ultralytics/ultralytics
- Deep Sort Realtime: https://github.com/leenhowe/Deep-SORT-realtime
- Flask: https://flask.palletsprojects.com/
