import customtkinter as ctk
from view.custom_teacher_window import CustomTeacherWindow
from view.custom_classroom_window import CustomClassroomWindow
from viewmodel.teacher_viewmodel import TeacherViewModel
from viewmodel.classroom_viewmodel import ClassroomViewModel
from service.json_service import JSONService

class CustomMainWindow(ctk.CTk):
    def __init__(self, teacher_vm, classroom_vm):
        super().__init__()
        
        # Настройка темы в образовательном стиле
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        self.title("🏫 School Management System")
        self.geometry("1300x750")
        self.teacher_vm = teacher_vm
        self.classroom_vm = classroom_vm
        
        self.create_sidebar()
        self.create_main_content()
        self.refresh_data()

    def create_sidebar(self):
        """Создание боковой панели в образовательном стиле"""
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#2c3e50")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Логотип школы
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(30, 20), padx=20, fill="x")
        
        ctk.CTkLabel(
            logo_frame, 
            text="🏫 ШКОЛА", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ecf0f1"
        ).pack()
        
        ctk.CTkLabel(
            logo_frame, 
            text="Управление", 
            font=ctk.CTkFont(size=14),
            text_color="#bdc3c7"
        ).pack()
        
        # Навигация
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(pady=30, padx=15, fill="x")
        
        nav_items = [
            ("👨‍🏫 Учителя", self.show_teachers_section, "#3498db"),
            ("👥 Классы", self.show_classrooms_section, "#2ecc71"),
            ("📚 Предметы", self.show_subjects_section, "#9b59b6"),
            ("📊 Отчеты", self.show_reports_section, "#e67e22")
        ]
        
        for text, command, color in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=self.adjust_color(color, -20),
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                corner_radius=8
            )
            btn.pack(pady=6, fill="x")
        
        # Быстрые действия
        quick_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        quick_frame.pack(pady=20, padx=15, fill="x")
        
        ctk.CTkLabel(
            quick_frame, 
            text="БЫСТРЫЕ ДЕЙСТВИЯ", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ecf0f1"
        ).pack(anchor="w", pady=(0, 10))
        
        quick_actions = [
            ("➕ Новый учитель", self.open_teachers_management),
            ("👥 Создать класс", self.open_classrooms_management)
        ]
        
        for text, command in quick_actions:
            btn = ctk.CTkButton(
                quick_frame,
                text=text,
                command=command,
                fg_color="transparent",
                border_color="#3498db",
                border_width=2,
                hover_color="#34495e",
                height=35,
                font=ctk.CTkFont(size=12)
            )
            btn.pack(pady=4, fill="x")
        
        # Статистика школы
        self.create_school_stats()
        
        # Переключатель темы
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.pack(side="bottom", pady=20, padx=15, fill="x")
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame, 
            text="Тёмная тема", 
            command=self.toggle_theme,
            progress_color="#3498db",
            onvalue="dark", 
            offvalue="light"
        )
        self.theme_switch.pack(pady=5, anchor="w")

    def create_school_stats(self):
        """Создание блока статистики школы"""
        stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        stats_frame.pack(pady=20, padx=15, fill="x")
        
        ctk.CTkLabel(
            stats_frame, 
            text="СТАТИСТИКА ШКОЛЫ", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ecf0f1"
        ).pack(anchor="w", pady=(0, 15))
        
        self.stats_cards = {}
        stats_data = [
            ("👨‍🏫 Учителей", "total_teachers", "#3498db"),
            ("👥 Классов", "total_classrooms", "#2ecc71"),
            ("📚 Учеников", "total_students", "#e67e22"),
            ("⭐ Высшая кат.", "high_category", "#9b59b6")
        ]
        
        for text, key, color in stats_data:
            card = ctk.CTkFrame(stats_frame, fg_color="#34495e", corner_radius=8)
            card.pack(fill="x", pady=5)
            
            content_frame = ctk.CTkFrame(card, fg_color="transparent")
            content_frame.pack(padx=12, pady=8, fill="x")
            
            ctk.CTkLabel(
                content_frame, 
                text=text, 
                font=ctk.CTkFont(size=11),
                text_color="#bdc3c7"
            ).pack(side="left")
            
            self.stats_cards[key] = ctk.CTkLabel(
                content_frame, 
                text="0", 
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=color
            )
            self.stats_cards[key].pack(side="right")

    def create_main_content(self):
        """Создание основного контента"""
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color="#ecf0f1")
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # Верхняя панель
        self.create_top_panel()
        
        # Контент
        self.create_content_area()

    def create_top_panel(self):
        """Создание верхней панели"""
        top_panel = ctk.CTkFrame(self.main_content, height=70, fg_color="#3498db", corner_radius=0)
        top_panel.pack(fill="x", padx=0, pady=0)
        top_panel.pack_propagate(False)
        
        # Заголовок раздела
        self.section_title = ctk.CTkLabel(
            top_panel,
            text="🏫 ОБЗОР ШКОЛЫ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.section_title.pack(side="left", padx=30, pady=23)
        
        # Поиск
        search_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        search_frame.pack(side="right", padx=30, pady=20)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Поиск учителей или классов...",
            width=280,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)

    def create_content_area(self):
        """Создание области контента"""
        # Приветственный баннер
        banner_frame = ctk.CTkFrame(self.main_content, fg_color="white", corner_radius=12)
        banner_frame.pack(fill="x", padx=20, pady=20)
        
        banner_content = ctk.CTkFrame(banner_frame, fg_color="transparent")
        banner_content.pack(padx=25, pady=20, fill="x")
        
        ctk.CTkLabel(
            banner_content,
            text="Добро пожаловать в систему управления школой",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2c3e50"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            banner_content,
            text="Эффективное управление учебным процессом",
            font=ctk.CTkFont(size=14),
            text_color="#7f8c8d"
        ).pack(anchor="w", pady=(5, 0))
        
        # Основная таблица
        self.create_main_table()

    def create_main_table(self):
        """Создание основной таблицы"""
        content_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Заголовок таблицы
        table_header = ctk.CTkFrame(content_frame, fg_color="transparent")
        table_header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            table_header, 
            text="👨‍🏫 ВСЕ УЧИТЕЛЯ", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2c3e50"
        ).pack(side="left")
        
        # Фильтры
        filter_frame = ctk.CTkFrame(table_header, fg_color="transparent")
        filter_frame.pack(side="right")
        
        self.subject_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Все предметы", "Математика", "Физика", "Литература", "История"],
            width=140,
            height=32
        )
        self.subject_filter.pack(side="left", padx=(0, 10))
        self.subject_filter.set("Все предметы")
        self.subject_filter.bind("<<ComboboxSelected>>", self.on_filter)
        
        # Таблица
        self.create_teachers_table(content_frame)

    def create_teachers_table(self, parent):
        """Создание таблицы учителей"""
        columns = ("ID", "ФИО", "Предмет", "Стаж", "Категория", "Телефон")
        self.tree_frame = ctk.CTkFrame(parent)
        self.tree_frame.pack(fill="both", expand=True)
        
        # Стилизация Treeview для светлой темы
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("School.Treeview", 
                       background="white",
                       foreground="#2c3e50",
                       fieldbackground="white",
                       rowheight=30,
                       font=('TkDefaultFont', 11))
        style.configure("School.Treeview.Heading", 
                       background="#3498db",
                       foreground="white",
                       relief="flat",
                       font=('TkDefaultFont', 12, 'bold'))
        style.map('School.Treeview', background=[('selected', '#2980b9')])
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", 
                               style="School.Treeview", height=18)
        
        # Настройка колонок
        column_config = {
            "ID": 70, "ФИО": 250, "Предмет": 120, 
            "Стаж": 80, "Категория": 100, "Телефон": 150
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

    def toggle_theme(self):
        """Переключение темы"""
        if self.theme_switch.get() == "dark":
            ctk.set_appearance_mode("dark")
            self.main_content.configure(fg_color="#1e1e1e")
        else:
            ctk.set_appearance_mode("light")
            self.main_content.configure(fg_color="#ecf0f1")

    def show_teachers_section(self):
        """Показать раздел учителей"""
        self.section_title.configure(text="👨‍🏫 УПРАВЛЕНИЕ УЧИТЕЛЯМИ")
        self.refresh_teachers_data()

    def show_classrooms_section(self):
        """Показать раздел классов"""
        self.section_title.configure(text="👥 УПРАВЛЕНИЕ КЛАССАМИ")
        self.refresh_classrooms_data()

    def show_subjects_section(self):
        """Показать раздел предметов"""
        self.section_title.configure(text="📚 УПРАВЛЕНИЕ ПРЕДМЕТАМИ")
        # Можно добавить функционал для управления предметами

    def show_reports_section(self):
        """Показать раздел отчетов"""
        self.section_title.configure(text="📊 ОТЧЕТЫ И СТАТИСТИКА")
        self.refresh_reports_display()

    def open_teachers_management(self):
        """Открыть управление учителями"""
        window = CustomTeacherWindow(self, self.teacher_vm)
        self.wait_window(window)
        self.refresh_data()

    def open_classrooms_management(self):
        """Открыть управление классами"""
        window = CustomClassroomWindow(self, self.classroom_vm, self.teacher_vm)
        self.wait_window(window)
        self.refresh_data()

    def on_search(self, event):
        """Обработка поиска"""
        self.refresh_data()

    def on_filter(self, event):
        """Обработка фильтра"""
        self.refresh_data()

    def refresh_data(self):
        """Обновление всех данных"""
        self.refresh_stats()
        self.refresh_teachers_data()

    def refresh_stats(self):
        """Обновление статистики"""
        total_teachers = len(self.teacher_vm.teachers)
        total_classrooms = len(self.classroom_vm.classrooms)
        total_students = sum(classroom.student_count for classroom in self.classroom_vm.classrooms)
        high_category = sum(1 for teacher in self.teacher_vm.teachers if teacher.category == "Высшая")
        
        self.stats_cards["total_teachers"].configure(text=str(total_teachers))
        self.stats_cards["total_classrooms"].configure(text=str(total_classrooms))
        self.stats_cards["total_students"].configure(text=str(total_students))
        self.stats_cards["high_category"].configure(text=str(high_category))

    def refresh_teachers_data(self):
        """Обновление данных учителей"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_entry.get().lower()
        subject_filter = self.subject_filter.get()
        
        for teacher in self.teacher_vm.teachers:
            if search_term and (search_term not in teacher.full_name.lower() and 
                              search_term not in teacher.subject.lower()):
                continue
                
            if subject_filter != "Все предметы" and teacher.subject != subject_filter:
                continue
            
            self.tree.insert("", "end", values=(
                teacher.id, teacher.full_name, teacher.subject, 
                f"{teacher.experience} лет", teacher.category, teacher.phone
            ))

    def refresh_classrooms_data(self):
        """Обновление данных классов"""
        # В реальном приложении можно переключать таблицу
        pass

    def refresh_reports_display(self):
        """Обновление отображения отчетов"""
        # В реальном приложении можно показать отчеты и графики
        pass

def main():
    json_service = JSONService()
    teacher_vm = TeacherViewModel(json_service)
    classroom_vm = ClassroomViewModel(teacher_vm, json_service)

    app = CustomMainWindow(teacher_vm, classroom_vm)
    app.mainloop()

if __name__ == "__main__":
    main()