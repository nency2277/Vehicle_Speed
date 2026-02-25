# Vehicle Speed Detection

Ứng dụng web phát hiện và theo dõi tốc độ xe cộ trong video sử dụng AI (YOLO + Deep Sort).

## 🎯 Tính năng

- **Phát hiện kendaraan thông minh**: Sử dụng mô hình YOLO (You Only Look Once) để phát hiện và nhận diện các loại xe cộ trên đường (ô tô, xe máy, xe tải, v.v.) với độ chính xác cao
  
- **Theo dõi kendaraan realtime**: Sử dụng thuật toán Deep Sort Tracker để theo dõi liên tục từng chiếc xe qua các frame liên tiếp, duy trì ID duy nhất cho mỗi xe

- **Tính toán tốc độ chính xác**: Tính toán vận tốc của các xe dựa trên khoảng cách di chuyển giữa các frame và khoảng thời gian, cho phép phát hiện xe vượt tốc độ

- **Giao diện web tương tác**: Ứng dụng Flask dễ sử dụng cho phép upload video từ trình duyệt và xem kết quả xử lý trực tiếp mà không cần dòng lệnh

- **Hiệu ứng cảnh báo**: Hình ảnh nhấp nháy (flash) để cảnh báo khi có xe vượt quá tốc độ quy định, giúp dễ dàng phát hiện người vi phạm

- **Hỗ trợ xử lý video linh hoạt**: Có thể xử lý video từ camera, file video, hoặc stream online

## 📋 Yêu cầu và Thư viện cần thiết

### Python
- **Python 3.8+** hoặc cao hơn

### Thư viện chính

|---------|---------|---------|
| **Flask** | >= 2.0.0 
| **OpenCV (cv2)** | >= 4.5.0 
| **NumPy** | >= 1.19.0 
| **Ultralytics YOLO** | >= 8.0.0
| **Deep Sort Realtime** | >= 1.0.0 
| **cvzone** | >= 1.5.0 
| **Werkzeug** | >= 2.0.0 
| **Pillow (PIL)** | >= 8.0.0 



### Chạy ứng dụng
```bash
python app.py
```

### Truy cập web interface
- Mở trình duyệt, truy cập: `http://localhost:5000`
- Upload file video
- Xem quá trình phát hiện và tính toán tốc độ realtime

