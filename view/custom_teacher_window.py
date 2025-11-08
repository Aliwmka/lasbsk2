import customtkinter as ctk
from tkinter import ttk, messagebox
from view.new_teacher_window import NewTeacherWindow

class CustomTeacherWindow(ctk.CTkToplevel):
    def __init__(self, parent, view_model):
        super().__init__(parent)
        self.title("👨‍🏫 Управление учителями")
        self.geometry("1100x650")
        self.vm = view_model
        
        self.create_interface()
        self.refresh_table()

    def create_interface(self):
        """Создание интерфейса управления учителями"""
        # Основной контейнер
        main_container = ctk.CTkFrame(self, fg_color="#ecf0f1")
        main_container.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Заголовок
        header_frame = ctk.CTkFrame(main_container, fg_color="#3498db", corner_radius=12)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(padx=25, pady=20, fill="x")
        
        ctk.CTkLabel(
            header_content,
            text="👨‍🏫 УПРАВЛЕНИЕ УЧИТЕЛЯМИ",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(side="left")
        
        # Кнопки действий
        actions_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        actions_frame.pack(side="right")
        
        action_buttons = [
            ("➕ Добавить учителя", self.add_teacher, "#27ae60"),
            ("✏️ Редактировать", self.edit_teacher, "#f39c12"),
            ("🗑️ Удалить", self.delete_teacher, "#e74c3c"),
            ("📊 Статистика", self.show_stats, "#9b59b6")
        ]
        
        for text, command, color in action_buttons:
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=self.adjust_color(color, -20),
                width=140,
                height=35,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            btn.pack(side="left", padx=5)
        
        # Панель поиска и фильтров
        self.create_search_panel(main_container)
        
        # Таблица
        self.create_table(main_container)

    def create_search_panel(self, parent):
        """Создание панели поиска"""
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Поиск
        search_left = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_left.pack(side="left", fill="x", expand=True)
        
        self.search_entry = ctk.CTkEntry(
            search_left,
            placeholder_text="🔍 Поиск по ФИО, предмету или телефону...",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Фильтры
        search_right = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_right.pack(side="right", padx=(20, 0))
        
        ctk.CTkLabel(
            search_right, 
            text="Фильтры:", 
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))
        
        self.subject_filter = ctk.CTkComboBox(
            search_right,
            values=["Все предметы", "Математика", "Физика", "Химия", "Биология", "История", 
                   "Литература", "Русский язык", "Иностранный язык", "География", "Информатика"],
            width=150,
            height=35
        )
        self.subject_filter.pack(side="left", padx=(0, 10))
        self.subject_filter.set("Все предметы")
        self.subject_filter.bind("<<ComboboxSelected>>", self.on_search)
        
        self.category_filter = ctk.CTkComboBox(
            search_right,
            values=["Все категории", "Высшая", "Первая", "Вторая", "Без категории"],
            width=140,
            height=35
        )
        self.category_filter.pack(side="left")
        self.category_filter.set("Все категории")
        self.category_filter.bind("<<ComboboxSelected>>", self.on_search)

    def create_table(self, parent):
        """Создание таблицы"""
        columns = ("ID", "ФИО", "Предмет", "Стаж", "Категория", "Телефон")
        self.tree_frame = ctk.CTkFrame(parent)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Стилизация Treeview
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Teacher.Treeview", 
                       background="white",
                       foreground="#2c3e50",
                       fieldbackground="white",
                       rowheight=35,
                       font=('TkDefaultFont', 11))
        style.configure("Teacher.Treeview.Heading", 
                       background="#3498db",
                       foreground="white",
                       relief="flat",
                       font=('TkDefaultFont', 12, 'bold'))
        style.map('Teacher.Treeview', background=[('selected', '#2980b9')])
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", 
                               style="Teacher.Treeview", height=15)
        
        # Настройка колонок
        column_config = {
            "ID": 80, "ФИО": 250, "Предмет": 150, 
            "Стаж": 100, "Категория": 120, "Телефон": 150
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_config[col])
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def adjust_color(self, color, amount):
        """Регулировка яркости цвета"""
        import colorsys
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        l = max(0, min(1, l + amount/255))
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

    def on_search(self, event=None):
        """Обработка поиска и фильтрации"""
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_entry.get().lower()
        subject_filter = self.subject_filter.get()
        category_filter = self.category_filter.get()
        
        for teacher in self.vm.teachers:
            # Поиск
            if search_term and (search_term not in teacher.full_name.lower() and 
                              search_term not in teacher.subject.lower() and
                              search_term not in teacher.phone.lower()):
                continue
            
            # Фильтр по предмету
            if subject_filter != "Все предметы" and teacher.subject != subject_filter:
                continue
            
            # Фильтр по категории
            if category_filter != "Все категории" and teacher.category != category_filter:
                continue
            
            self.tree.insert("", "end", values=(
                teacher.id, teacher.full_name, teacher.subject, 
                f"{teacher.experience} лет", teacher.category, teacher.phone
            ))

    def get_selected_id(self):
        """Получить ID выбранного учителя"""
        selection = self.tree.selection()
        return int(self.tree.item(selection[0])["values"][0]) if selection else None

    def add_teacher(self):
        """Добавить учителя"""
        dialog = NewTeacherWindow(self)
        self.wait_window(dialog)
        if dialog.result:
            try:
                self.vm.add_teacher(
                    full_name=dialog.result["full_name"],
                    subject=dialog.result["subject"],
                    experience=dialog.result["experience"],
                    category=dialog.result["category"],
                    phone=dialog.result["phone"]
                )
                self.refresh_table()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def edit_teacher(self):
        """Редактировать учителя"""
        teacher_id = self.get_selected_id()
        if not teacher_id:
            messagebox.showwarning("Внимание", "Выберите учителя для редактирования.")
            return
        
        try:
            teacher = self.vm.get_teacher_by_id(teacher_id)
            dialog = NewTeacherWindow(
                self,
                teacher_id=teacher.id,
                full_name=teacher.full_name,
                subject=teacher.subject,
                experience=teacher.experience,
                category=teacher.category,
                phone=teacher.phone
            )
            self.wait_window(dialog)
            if dialog.result:
                self.vm.update_teacher(
                    teacher_id=teacher_id,
                    full_name=dialog.result["full_name"],
                    subject=dialog.result["subject"],
                    experience=dialog.result["experience"],
                    category=dialog.result["category"],
                    phone=dialog.result["phone"]
                )
                self.refresh_table()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_teacher(self):
        """Удалить учителя"""
        teacher_id = self.get_selected_id()
        if not teacher_id:
            messagebox.showwarning("Внимание", "Выберите учителя для удаления.")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранного учителя?"):
            try:
                self.vm.delete_teacher(teacher_id)
                self.refresh_table()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def show_stats(self):
        """Показать статистику по учителям"""
        total_teachers = len(self.vm.teachers)
        
        # Статистика по предметам
        subject_stats = {}
        for teacher in self.vm.teachers:
            if teacher.subject not in subject_stats:
                subject_stats[teacher.subject] = 0
            subject_stats[teacher.subject] += 1
        
        # Статистика по категориям
        category_stats = {}
        for teacher in self.vm.teachers:
            if teacher.category not in category_stats:
                category_stats[teacher.category] = 0
            category_stats[teacher.category] += 1
        
        # Создаем окно статистики
        stats_window = ctk.CTkToplevel(self)
        stats_window.title("📊 Статистика учителей")
        stats_window.geometry("500x500")
        stats_window.transient(self)
        stats_window.grab_set()
        
        main_frame = ctk.CTkFrame(stats_window, fg_color="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="📊 СТАТИСТИКА УЧИТЕЛЕЙ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2c3e50"
        ).pack(pady=(0, 20))
        
        # Основная статистика
        stats_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=8)
        stats_frame.pack(fill="x", pady=10, padx=10)
        
        stats_data = [
            ("Всего учителей:", str(total_teachers), "#3498db"),
            ("Средний стаж:", f"{sum(t.experience for t in self.vm.teachers) / total_teachers:.1f} лет", "#27ae60")
        ]
        
        for text, value, color in stats_data:
            stat_row = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_row.pack(fill="x", padx=15, pady=8)
            
            ctk.CTkLabel(
                stat_row,
                text=text,
                font=ctk.CTkFont(size=14),
                text_color="#7f8c8d"
            ).pack(side="left")
            
            ctk.CTkLabel(
                stat_row,
                text=value,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color
            ).pack(side="right")
        
        # Статистика по предметам
        subjects_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=8)
        subjects_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        ctk.CTkLabel(
            subjects_frame,
            text="Распределение по предметам:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2c3e50"
        ).pack(pady=10)
        
        for subject, count in subject_stats.items():
            subject_row = ctk.CTkFrame(subjects_frame, fg_color="transparent")
            subject_row.pack(fill="x", padx=15, pady=4)
            
            ctk.CTkLabel(
                subject_row,
                text=subject,
                font=ctk.CTkFont(size=12),
                text_color="#7f8c8d"
            ).pack(side="left")
            
            ctk.CTkLabel(
                subject_row,
                text=str(count),
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#3498db"
            ).pack(side="right")