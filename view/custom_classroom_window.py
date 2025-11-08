import customtkinter as ctk
from tkinter import ttk, messagebox
from view.new_classroom_window import NewClassroomWindow

class CustomClassroomWindow(ctk.CTkToplevel):
    def __init__(self, parent, classroom_vm, teacher_vm):
        super().__init__(parent)
        self.title("👥 Управление классами")
        self.geometry("1200x700")
        self.classroom_vm = classroom_vm
        self.teacher_vm = teacher_vm
        
        self.create_interface()
        self.refresh_table()

    def create_interface(self):
        """Создание интерфейса управления классами"""
        # Основной контейнер
        main_container = ctk.CTkFrame(self, fg_color="#ecf0f1")
        main_container.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Заголовок
        header_frame = ctk.CTkFrame(main_container, fg_color="#2ecc71", corner_radius=12)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(padx=25, pady=20, fill="x")
        
        ctk.CTkLabel(
            header_content,
            text="👥 УПРАВЛЕНИЕ КЛАССАМИ",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(side="left")
        
        # Кнопки действий
        actions_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        actions_frame.pack(side="right")
        
        action_buttons = [
            ("➕ Создать класс", self.add_classroom, "#27ae60"),
            ("✏️ Редактировать", self.edit_classroom, "#f39c12"),
            ("🗑️ Удалить", self.delete_classroom, "#e74c3c"),
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
            placeholder_text="🔍 Поиск по названию класса или руководителю...",
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
        
        # Фильтр по уровню
        self.grade_filter = ctk.CTkComboBox(
            search_right,
            values=["Все уровни", "1 класс", "2 класс", "3 класс", "4 класс", "5 класс", 
                   "6 класс", "7 класс", "8 класс", "9 класс", "10 класс", "11 класс"],
            width=120,
            height=35
        )
        self.grade_filter.pack(side="left", padx=(0, 10))
        self.grade_filter.set("Все уровни")
        self.grade_filter.bind("<<ComboboxSelected>>", self.on_search)
        
        # Фильтр по классному руководителю
        teacher_names = ["Все руководители"] + [teacher.full_name for teacher in self.teacher_vm.teachers]
        self.teacher_filter = ctk.CTkComboBox(
            search_right,
            values=teacher_names,
            width=180,
            height=35
        )
        self.teacher_filter.pack(side="left")
        self.teacher_filter.set("Все руководители")
        self.teacher_filter.bind("<<ComboboxSelected>>", self.on_search)

    def create_table(self, parent):
        """Создание таблицы"""
        columns = ("ID", "Класс", "Классный руководитель", "Кол-во учеников", "Уровень")
        self.tree_frame = ctk.CTkFrame(parent)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Стилизация Treeview
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Classroom.Treeview", 
                       background="white",
                       foreground="#2c3e50",
                       fieldbackground="white",
                       rowheight=35,
                       font=('TkDefaultFont', 11))
        style.configure("Classroom.Treeview.Heading", 
                       background="#2ecc71",
                       foreground="white",
                       relief="flat",
                       font=('TkDefaultFont', 12, 'bold'))
        style.map('Classroom.Treeview', background=[('selected', '#27ae60')])
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", 
                               style="Classroom.Treeview", height=16)
        
        # Настройка колонок
        column_config = {
            "ID": 80, "Класс": 120, "Классный руководитель": 250, 
            "Кол-во учеников": 120, "Уровень": 100
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
        grade_filter = self.grade_filter.get()
        teacher_filter = self.teacher_filter.get()
        
        # Создаем словарь для быстрого доступа к учителям
        teacher_map = {teacher.id: teacher.full_name for teacher in self.teacher_vm.teachers}
        
        for classroom in self.classroom_vm.classrooms:
            teacher_name = teacher_map.get(classroom.teacher_id, "Неизвестно")
            
            # Поиск
            if search_term and (search_term not in classroom.class_name.lower() and 
                              search_term not in teacher_name.lower()):
                continue
            
            # Фильтр по уровню
            if grade_filter != "Все уровни":
                required_grade = int(grade_filter.split()[0])
                if classroom.grade_level != required_grade:
                    continue
            
            # Фильтр по классному руководителю
            if teacher_filter != "Все руководители" and teacher_name != teacher_filter:
                continue
            
            self.tree.insert("", "end", values=(
                classroom.id, classroom.class_name, teacher_name, 
                classroom.student_count, f"{classroom.grade_level} класс"
            ))

    def get_selected_id(self):
        """Получить ID выбранного класса"""
        selection = self.tree.selection()
        return int(self.tree.item(selection[0])["values"][0]) if selection else None

    def add_classroom(self):
        """Добавить класс"""
        dialog = NewClassroomWindow(self, self.teacher_vm.teachers)
        self.wait_window(dialog)
        if dialog.result:
            try:
                self.classroom_vm.add_classroom(
                    class_name=dialog.result["class_name"],
                    teacher_id=dialog.result["teacher_id"],
                    student_count=dialog.result["student_count"],
                    grade_level=dialog.result["grade_level"]
                )
                self.refresh_table()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def edit_classroom(self):
        """Редактировать класс"""
        classroom_id = self.get_selected_id()
        if not classroom_id:
            messagebox.showwarning("Внимание", "Выберите класс для редактирования.")
            return
        
        try:
            classroom = self.classroom_vm.get_classroom_by_id(classroom_id)
            dialog = NewClassroomWindow(
                self,
                self.teacher_vm.teachers,
                classroom_id=classroom.id,
                class_name=classroom.class_name,
                teacher_id=classroom.teacher_id,
                student_count=classroom.student_count,
                grade_level=classroom.grade_level
            )
            self.wait_window(dialog)
            if dialog.result:
                self.classroom_vm.update_classroom(
                    classroom_id=classroom_id,
                    class_name=dialog.result["class_name"],
                    teacher_id=dialog.result["teacher_id"],
                    student_count=dialog.result["student_count"],
                    grade_level=dialog.result["grade_level"]
                )
                self.refresh_table()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_classroom(self):
        """Удалить класс"""
        classroom_id = self.get_selected_id()
        if not classroom_id:
            messagebox.showwarning("Внимание", "Выберите класс для удаления.")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный класс?"):
            try:
                self.classroom_vm.delete_classroom(classroom_id)
                self.refresh_table()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def show_stats(self):
        """Показать статистику по классам"""
        total_classrooms = len(self.classroom_vm.classrooms)
        total_students = sum(classroom.student_count for classroom in self.classroom_vm.classrooms)
        avg_students = total_students / total_classrooms if total_classrooms > 0 else 0
        
        # Статистика по уровням
        grade_stats = {}
        for classroom in self.classroom_vm.classrooms:
            if classroom.grade_level not in grade_stats:
                grade_stats[classroom.grade_level] = {"count": 0, "students": 0}
            grade_stats[classroom.grade_level]["count"] += 1
            grade_stats[classroom.grade_level]["students"] += classroom.student_count
        
        # Создаем окно статистики
        stats_window = ctk.CTkToplevel(self)
        stats_window.title("📊 Статистика классов")
        stats_window.geometry("500x550")
        stats_window.transient(self)
        stats_window.grab_set()
        
        main_frame = ctk.CTkFrame(stats_window, fg_color="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="📊 СТАТИСТИКА КЛАССОВ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2c3e50"
        ).pack(pady=(0, 20))
        
        # Основная статистика
        stats_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=8)
        stats_frame.pack(fill="x", pady=10, padx=10)
        
        stats_data = [
            ("Всего классов:", str(total_classrooms), "#3498db"),
            ("Всего учеников:", str(total_students), "#2ecc71"),
            ("Среднее в классе:", f"{avg_students:.1f} учеников", "#e67e22")
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
        
        # Статистика по уровням
        grades_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=8)
        grades_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        ctk.CTkLabel(
            grades_frame,
            text="Распределение по уровням:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2c3e50"
        ).pack(pady=10)
        
        for grade_level in sorted(grade_stats.keys()):
            stats = grade_stats[grade_level]
            grade_row = ctk.CTkFrame(grades_frame, fg_color="transparent")
            grade_row.pack(fill="x", padx=15, pady=4)
            
            ctk.CTkLabel(
                grade_row,
                text=f"{grade_level} класс:",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#3498db"
            ).pack(side="left")
            
            info_frame = ctk.CTkFrame(grade_row, fg_color="transparent")
            info_frame.pack(side="right")
            
            ctk.CTkLabel(
                info_frame,
                text=f"{stats['count']} классов",
                font=ctk.CTkFont(size=11),
                text_color="#7f8c8d"
            ).pack(side="left", padx=(0, 10))
            
            ctk.CTkLabel(
                info_frame,
                text=f"{stats['students']} учеников",
                font=ctk.CTkFont(size=11),
                text_color="#27ae60"
            ).pack(side="left")