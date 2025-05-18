import tkinter as tk
from time import perf_counter
from turtle import RawTurtle, ScrolledCanvas, TurtleScreen
from map_utils import Map

class App:
    def __init__(self, root):
        self.root = root
        root.title("A* Pathfinding")
        
        # Left: Canvas chứa turtle
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.cv = ScrolledCanvas(self.canvas_frame, width=600, height=800)
        self.cv.pack(fill=tk.BOTH, expand=True)
        self.screen = TurtleScreen(self.cv)      # <-- từ turtle, không phải tk
        self.screen.mode("world")
        self.screen.setworldcoordinates(-410, -710, 410, 710)
        self.t = RawTurtle(self.screen, shape='turtle')
        self.t.hideturtle()    # ẩn luôn khi tạo
        self.t1 = RawTurtle(self.screen, shape='turtle')
        self.t1.hideturtle()    # ẩn luôn khi tạo
        
        # Right: Controls & Legend
        ctrl = tk.Frame(root, padx=10, pady=10)
        ctrl.pack(side=tk.RIGHT, fill=tk.Y)
        
        
        # --- Thêm input kích thước map ---
        tk.Label(ctrl, text="Nhập kích thước bản đồ:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0,5))
        size_frame = tk.Frame(ctrl)
        size_frame.pack(fill=tk.X, pady=(0,20))
        tk.Label(size_frame, text="Chiều cao (m):").grid(row=0, column=0, sticky='w')
        self.entry_m = tk.Entry(size_frame, width=5)
        self.entry_m.grid(row=0, column=1, sticky='w')
        self.entry_m.insert(0, "10")  # mặc định 10

        tk.Label(size_frame, text="Chiều rộng (n):").grid(row=1, column=0, sticky='w')
        self.entry_n = tk.Entry(size_frame, width=5)
        self.entry_n.grid(row=1, column=1, sticky='w')
        self.entry_n.insert(0, "10")  # mặc định 10
        
        # Start button
        self.btn_start = tk.Button(ctrl, text="Bắt đầu giải", command=self.start)
        self.btn_start.pack(fill=tk.X, pady=5)
        # Legend
        tk.Label(ctrl, text="Chú thích:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(20,5))
        self._add_legend(ctrl, "Đích đến", 'orange')
        self._add_legend(ctrl, "Vật cản / Tường", 'black')
        self._add_legend(ctrl, "Điểm xuất phát", 'green')
        self._add_legend(ctrl, "Giải thuật A*", 'blue')
        self._add_legend(ctrl, "Giải thuật Breadth first search", 'red')
        self._add_legend(ctrl, "Đường đi chung", 'purple')
        
        # Info & finish/reset buttons (ẩn ban đầu)
        self.info_label = tk.Label(ctrl, text="", wraplength=200, justify='left')
        self.btn_finish = tk.Button(ctrl, text="Hoàn tất", command=root.quit)
        self.btn_reset  = tk.Button(ctrl, text="Quay lại", command=self.reset)
        
        # Prepare map & turtle
        self.width_half, self.height_half = 400, 700
        #self._prepare_map()
        
    
    def _add_legend(self, parent, label, color):
        f = tk.Frame(parent)
        f.pack(anchor='w', pady=2)
        c = tk.Canvas(f, width=20, height=20)
        c.pack(side=tk.LEFT)

        if label == "Giải thuật A*" or label == "Giải thuật Breadth first search" or label == "Đường đi chung":
            # Vẽ đường thẳng ngang (line)
            c.create_line(2, 10, 18, 10, fill=color, width=3)
        else:
            # Vẽ hình tròn (oval)
            c.create_oval(2, 2, 18, 18, fill=color, outline=color)

        tk.Label(f, text=label).pack(side=tk.RIGHT, padx=5)
    
    def _prepare_map(self):
        self.btn_start.config(state=tk.DISABLED)
        self.entry_m.config(state='disabled')
        self.entry_n.config(state='disabled')
        try:
            m = int(self.entry_m.get())  # đọc chiều cao map từ Entry
            n = int(self.entry_n.get())  # đọc chiều rộng map từ Entry
            if m <= 0 or n <= 0:
                raise ValueError
        except Exception:
            tk.messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập số nguyên dương cho kích thước bản đồ!")
            self.btn_start.config(state=tk.NORMAL)
            return
        # khởi tạo bản đồ, start/goal
        self.mmap = Map.map_init(m,n)
        self.goals = Map.map_random(self.mmap)   # list of 3 goals
        self.start = Map.random_curpos(self.mmap)
        # vẽ grid + obstacles + goals
        self.t.clear()
        self.t1.clear()
        Map.draw_map(self.mmap, 'pink', self.t, self.width_half, self.height_half, self.start)
        # place turtle at start
        sx, sy = Map.turn2pixel(self.mmap, self.height_half, self.width_half, *self.start)
        self.t.up(); self.t.goto(sx, sy); self.t.down()
        self.t1.up(); self.t1.goto(sx, sy); self.t1.down()
        
        self.t.showturtle()
        self.t1.showturtle()
    
        self.btn_start.config(state=tk.NORMAL)
    
    def start(self):
        self._prepare_map()
        self.btn_start.config(state=tk.DISABLED)
        t0 = perf_counter()
        result = Map.run(self.t, self.t1, self.mmap, self.width_half, self.height_half, self.start, self.goals)
        dt = perf_counter() - t0
        
        if result is False:
            info_text = f"Giải mã thất bại!\nThời gian giải mã: {dt:.3f} giây"
            self.info_label.config(text=info_text, fg="red")
        else:
            t_a_start, t_bfs = result
            info_text = (f"Giải mã thành công!\n"
                        f"Tổng thời gian thực thi: {dt:.3f} giây\n"
                        f"Thời gian A*: {t_a_start:.5f} giây\n"
                        f"Thời gian BFS: {t_bfs:.5f} giây")
            self.info_label.config(text=info_text, fg="green")
            
        self.btn_start.config(state=tk.DISABLED)
        # hiện info + nút finish/reset
        self.info_label.pack(pady=(20,5))
        self.btn_finish.pack(fill=tk.X, pady=2)
        self.btn_reset.pack(fill=tk.X, pady=2)
    def reset(self):
        # ẩn info & nút finish/reset, hiện lại start
        self.info_label.pack_forget()
        self.btn_finish.pack_forget()
        self.btn_reset.pack_forget()
        self.btn_start.config(state=tk.NORMAL)
        self.t.hideturtle()    # ẩn luôn khi tạo
        self.t1.hideturtle()    # ẩn luôn khi tạo
        self.entry_m.config(state='normal')
        self.entry_n.config(state='normal')
        # reset map & redraw
        #self._prepare_map()