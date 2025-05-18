# 🧭 PathRider Ver2 – A* & BFS Pathfinding Visualizer with Turtle

PathRider Ver2 là một ứng dụng mô phỏng hai thuật toán tìm đường A* và Breadth-First Search (BFS) với giao diện trực quan bằng `turtle` và `tkinter`. Cho phép người dùng nhập kích thước bản đồ, sinh ngẫu nhiên vật cản và mục tiêu, và quan sát trực tiếp quá trình tìm đường.

---

## 🚀 Tính năng

- ✅ Nhập kích thước bản đồ (m x n) tùy chỉnh.
- 🧱 Tự động sinh vật cản và 3 điểm đích ngẫu nhiên.
- 🧠 Giải thuật tìm đường: A* (màu xanh) và BFS (màu đỏ).
- ⏱ So sánh thời gian thực thi giữa A* và BFS.
- 🎯 Hiển thị đường đi chung (màu tím) khi cả hai thuật toán cùng tìm được.
- 🖥 Giao diện đồ họa dễ sử dụng bằng `tkinter`.

---

---

## ⚙️ Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/Capopata/A_Star-Navigator_Ver2.git
cd A_Star-Navigator_Ver2
```

### 2. Cài đặt thư viện (nếu cần)

```bash
pip install -r requirements.txt
```

> **Lưu ý**: Ứng dụng sử dụng các thư viện chuẩn của Python (`tkinter`, `turtle`, `random`, `heapq`, `time`). Nếu dùng Python bản đầy đủ, không cần cài thêm gì.

---

## ▶️ Cách sử dụng

1. Chạy ứng dụng:

```bash
python main.py
```

2. Trong giao diện:

- Nhập chiều cao (`m`) và chiều rộng (`n`) của bản đồ.
- Nhấn **"Bắt đầu giải"** để sinh bản đồ và mô phỏng đường đi.
- Theo dõi đường đi của từng thuật toán và thời gian giải quyết.

---

## 📁 Cấu trúc thư mục

```
A_Star-Navigator_Ver2/
├── main.py                 # Giao diện và luồng chính
├── map.py                  # Sinh bản đồ, điểm start/goal
├── pathfinding.py          # Thuật toán A* và BFS
├── utils.py                # Các hàm hỗ trợ
├── requirements.txt
└── README.md
```

---

## 📌 Ghi chú

- Ứng dụng dùng `ScrolledCanvas` để đảm bảo vùng vẽ hiển thị tốt ngay cả với bản đồ lớn.
- Rùa thứ 2 (`t1`) sẽ chỉ xuất hiện sau khi bản đồ được sinh thành công.

---

## 👨‍💻 Tác giả

- Dự án được phát triển bởi [Capopata](https://github.com/Capopata).
