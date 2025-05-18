# A_Star-Navigator_Ver2

Ứng dụng mô phỏng thuật toán tìm đường A* và BFS sử dụng thư viện `turtle` trong Python. Người dùng có thể nhập kích thước bản đồ, quan sát quá trình tìm đường của hai thuật toán và so sánh hiệu suất của chúng.

## 🚀 Tính năng

- Tạo bản đồ tùy chỉnh với kích thước m x n.
- Tự động sinh vật cản và điểm đích.
- Hiển thị trực quan đường đi của A* (màu xanh) và BFS (màu đỏ).
- So sánh thời gian thực thi của hai thuật toán.
- Giao diện người dùng đơn giản với `tkinter`.

## 🖼️ Giao diện

![Giao diện chính](https://github.com/Capopata/A_Star-Navigator_Ver2/blob/main/screenshot.png)

## 🛠️ Cài đặt

1. Clone repository:

```bash
git clone https://github.com/Capopata/A_Star-Navigator_Ver2.git
cd A_Star-Navigator_Ver2
```
2. Cài đặt thư viện
- pip install -r requirements.txt
3. Cách sử dụng
- Chạy ứng dụng : python main.py
- Trong giao diện chính:
  + Nhập chiều cao (m) và chiều rộng (n) cho bản đồ.
  + Nhấn "Bắt đầu giải" để bắt đầu quá trình tìm đường.
  + Quan sát quá trình tìm đường và so sánh thời gian thực thi.
4. Cấu trúc thư mục
A_Star-Navigator_Ver2/
├── main.py
├── map.py
├── pathfinding.py
├── utils.py
├── README.md
└── requirements.txt
