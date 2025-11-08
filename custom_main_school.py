import customtkinter as ctk
from view.custom_teacher_window import CustomTeacherWindow
from view.custom_classroom_window import CustomClassroomWindow
from viewmodel.teacher_viewmodel import TeacherViewModel
from viewmodel.classroom_viewmodel import ClassroomViewModel
from service.json_service import JSONService
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

class CustomMainWindow(ctk.CTk):
    def __init__(self, teacher_vm, classroom_vm):
        super().__init__()
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        self.title("🏫 School Management System")
        self.geometry("1300x750")
        self.teacher_vm = teacher_vm
        self.classroom_vm = classroom_vm
        self.current_section = "teachers"
        
        self.create_sidebar()
        self.create_main_content()
        self.refresh_data()

    def create_sidebar(self):
        """Создание боковой панели"""
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#2c3e50")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Логотип
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
            ("👨‍🏫 Учителя", "teachers", "#3498db"),
            ("👥 Классы", "classrooms", "#2ecc71"),
            ("📊 Отчеты", "reports", "#9b59b6")
        ]
        
        self.nav_buttons = {}
        for text, section, color in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=lambda s=section: self.show_section(s),
                fg_color=color,
                hover_color=self.adjust_color(color, -20),
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                corner_radius=8
            )
            btn.pack(pady=6, fill="x")
            self.nav_buttons[section] = btn
        
        # Статистика школы
        self.create_school_stats()
        
        # Переключатель темы
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.pack(side="bottom", pady=20, padx=15, fill="x")
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame, 
            text="Тёмная тема", 
            command=self.toggle_theme,
            progress_color="#3498db"
        )
        self.theme_switch.pack(pady=5, anchor="w")

    def create_school_stats(self):
        """Создание блока статистики"""
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
        
        # Создаем фреймы для разных разделов
        self.teachers_frame = ctk.CTkFrame(self.main_content, corner_radius=0)
        self.classrooms_frame = ctk.CTkFrame(self.main_content, corner_radius=0)
        self.reports_frame = ctk.CTkFrame(self.main_content, corner_radius=0)
        
        self.create_teachers_section()
        self.create_classrooms_section()
        self.create_reports_section()
        
        # Показываем начальный раздел
        self.show_section("teachers")

    def create_teachers_section(self):
        """Создание раздела учителей"""
        # Верхняя панель
        top_panel = ctk.CTkFrame(self.teachers_frame, height=70, fg_color="#3498db", corner_radius=0)
        top_panel.pack(fill="x")
        top_panel.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            top_panel,
            text="👨‍🏫 УПРАВЛЕНИЕ УЧИТЕЛЯМИ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=30, pady=23)
        
        actions_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        actions_frame.pack(side="right", padx=30, pady=20)
        
        ctk.CTkButton(
            actions_frame,
            text="➕ Добавить учителя",
            command=self.open_teachers_management,
            fg_color="#27ae60",
            hover_color="#219a52",
            width=140,
            height=35
        ).pack(side="left", padx=5)
        
        # Поиск
        search_frame = ctk.CTkFrame(self.teachers_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=15)
        
        self.teachers_search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Поиск учителей...",
            height=35
        )
        self.teachers_search_entry.pack(side="left", fill="x", expand=True)
        self.teachers_search_entry.bind("<KeyRelease>", lambda e: self.refresh_teachers_data())
        
        # Таблица учителей
        self.create_teachers_table()

    def create_classrooms_section(self):
        """Создание раздела классов"""
        top_panel = ctk.CTkFrame(self.classrooms_frame, height=70, fg_color="#2ecc71", corner_radius=0)
        top_panel.pack(fill="x")
        top_panel.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            top_panel,
            text="👥 УПРАВЛЕНИЕ КЛАССАМИ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=30, pady=23)
        
        actions_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        actions_frame.pack(side="right", padx=30, pady=20)
        
        ctk.CTkButton(
            actions_frame,
            text="➕ Создать класс",
            command=self.open_classrooms_management,
            fg_color="#27ae60",
            hover_color="#219a52",
            width=140,
            height=35
        ).pack(side="left", padx=5)
        
        search_frame = ctk.CTkFrame(self.classrooms_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=15)
        
        self.classrooms_search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Поиск классов...",
            height=35
        )
        self.classrooms_search_entry.pack(side="left", fill="x", expand=True)
        self.classrooms_search_entry.bind("<KeyRelease>", lambda e: self.refresh_classrooms_data())
        
        # Таблица классов
        self.create_classrooms_table()

    def create_reports_section(self):
        """Создание раздела отчетов"""
        top_panel = ctk.CTkFrame(self.reports_frame, height=70, fg_color="#9b59b6", corner_radius=0)
        top_panel.pack(fill="x")
        top_panel.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            top_panel,
            text="📊 ОТЧЕТЫ И СТАТИСТИКА",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=30, pady=23)
        
        # Кнопки отчетов
        reports_buttons_frame = ctk.CTkFrame(self.reports_frame, fg_color="transparent")
        reports_buttons_frame.pack(pady=20)
        
        reports = [
            ("👨‍🏫 Статистика учителей", self.show_teachers_stats),
            ("👥 Статистика классов", self.show_classrooms_stats),
            ("📚 Распределение по предметам", self.show_subjects_stats)
        ]
        
        for text, command in reports:
            ctk.CTkButton(
                reports_buttons_frame,
                text=text,
                command=command,
                width=200,
                height=40,
                font=ctk.CTkFont(size=12)
            ).pack(pady=5)
        
        # Фрейм для графиков
        self.chart_frame = ctk.CTkFrame(self.reports_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def create_teachers_table(self):
        """Создание таблицы учителей"""
        columns = ("ID", "ФИО", "Предмет", "Стаж", "Категория", "Телефон")
        
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Teachers.Treeview", 
                       background="white",
                       foreground="#2c3e50",
                       fieldbackground="white",
                       rowheight=30)
        style.configure("Teachers.Treeview.Heading", 
                       background="#3498db",
                       foreground="white",
                       relief="flat")
        style.map('Teachers.Treeview', background=[('selected', '#2980b9')])
        
        self.teachers_tree = ttk.Treeview(self.teachers_frame, columns=columns, show="headings", 
                                        style="Teachers.Treeview", height=15)
        
        column_config = {
            "ID": 70, "ФИО": 250, "Предмет": 120, 
            "Стаж": 80, "Категория": 100, "Телефон": 150
        }
        
        for col in columns:
            self.teachers_tree.heading(col, text=col)
            self.teachers_tree.column(col, width=column_config[col])
        
        scrollbar = ttk.Scrollbar(self.teachers_frame, orient="vertical", command=self.teachers_tree.yview)
        self.teachers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.teachers_tree.pack(fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)

    def create_classrooms_table(self):
        """Создание таблицы классов"""
        columns = ("ID", "Класс", "Классный руководитель", "Учеников", "Уровень")
        
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Classrooms.Treeview", 
                       background="white",
                       foreground="#2c3e50",
                       fieldbackground="white",
                       rowheight=30)
        style.configure("Classrooms.Treeview.Heading", 
                       background="#2ecc71",
                       foreground="white",
                       relief="flat")
        style.map('Classrooms.Treeview', background=[('selected', '#27ae60')])
        
        self.classrooms_tree = ttk.Treeview(self.classrooms_frame, columns=columns, show="headings", 
                                          style="Classrooms.Treeview", height=15)
        
        column_config = {
            "ID": 70, "Класс": 80, "Классный руководитель": 250, 
            "Учеников": 100, "Уровень": 80
        }
        
        for col in columns:
            self.classrooms_tree.heading(col, text=col)
            self.classrooms_tree.column(col, width=column_config[col])
        
        scrollbar = ttk.Scrollbar(self.classrooms_frame, orient="vertical", command=self.classrooms_tree.yview)
        self.classrooms_tree.configure(yscrollcommand=scrollbar.set)
        
        self.classrooms_tree.pack(fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)

    def show_section(self, section):
        """Показать выбранный раздел"""
        # Скрыть все разделы
        self.teachers_frame.pack_forget()
        self.classrooms_frame.pack_forget()
        self.reports_frame.pack_forget()
        
        # Сбросить цвета кнопок
        for btn in self.nav_buttons.values():
            btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        # Показать выбранный раздел и подсветить кнопку
        if section == "teachers":
            self.teachers_frame.pack(fill="both", expand=True)
            self.nav_buttons["teachers"].configure(fg_color="#3498db")
            self.refresh_teachers_data()
        elif section == "classrooms":
            self.classrooms_frame.pack(fill="both", expand=True)
            self.nav_buttons["classrooms"].configure(fg_color="#2ecc71")
            self.refresh_classrooms_data()
        elif section == "reports":
            self.reports_frame.pack(fill="both", expand=True)
            self.nav_buttons["reports"].configure(fg_color="#9b59b6")
        
        self.current_section = section

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
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
            self.main_content.configure(fg_color="#1e1e1e")
        else:
            ctk.set_appearance_mode("light")
            self.main_content.configure(fg_color="#ecf0f1")

    def refresh_data(self):
        """Обновление всех данных"""
        self.refresh_stats()
        if self.current_section == "teachers":
            self.refresh_teachers_data()
        elif self.current_section == "classrooms":
            self.refresh_classrooms_data()

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
        for item in self.teachers_tree.get_children():
            self.teachers_tree.delete(item)
        
        search_term = self.teachers_search_entry.get().lower() if hasattr(self, 'teachers_search_entry') else ""
        
        for teacher in self.teacher_vm.teachers:
            if search_term and (search_term not in teacher.full_name.lower() and 
                              search_term not in teacher.subject.lower()):
                continue
            
            self.teachers_tree.insert("", "end", values=(
                teacher.id, teacher.full_name, teacher.subject, 
                f"{teacher.experience} лет", teacher.category, teacher.phone
            ))

    def refresh_classrooms_data(self):
        """Обновление данных классов"""
        for item in self.classrooms_tree.get_children():
            self.classrooms_tree.delete(item)
        
        search_term = self.classrooms_search_entry.get().lower() if hasattr(self, 'classrooms_search_entry') else ""
        
        # Создаем словарь для быстрого доступа к учителям
        teacher_map = {teacher.id: teacher.full_name for teacher in self.teacher_vm.teachers}
        
        for classroom in self.classroom_vm.classrooms:
            teacher_name = teacher_map.get(classroom.teacher_id, "Неизвестно")
            
            if search_term and (search_term not in classroom.class_name.lower() and 
                              search_term not in teacher_name.lower()):
                continue
            
            self.classrooms_tree.insert("", "end", values=(
                classroom.id, classroom.class_name, teacher_name, 
                classroom.student_count, f"{classroom.grade_level} класс"
            ))

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

    def show_teachers_stats(self):
        """Показать статистику учителей"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Анализ данных учителей
        subjects = {}
        categories = {}
        experience_ranges = {"0-5 лет": 0, "6-10 лет": 0, "11-20 лет": 0, "20+ лет": 0}
        
        for teacher in self.teacher_vm.teachers:
            # По предметам
            if teacher.subject not in subjects:
                subjects[teacher.subject] = 0
            subjects[teacher.subject] += 1
            
            # По категориям
            if teacher.category not in categories:
                categories[teacher.category] = 0
            categories[teacher.category] += 1
            
            # По стажу
            if teacher.experience <= 5:
                experience_ranges["0-5 лет"] += 1
            elif teacher.experience <= 10:
                experience_ranges["6-10 лет"] += 1
            elif teacher.experience <= 20:
                experience_ranges["11-20 лет"] += 1
            else:
                experience_ranges["20+ лет"] += 1
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Диаграмма по предметам
        if subjects:
            ax1.pie(subjects.values(), labels=subjects.keys(), autopct='%1.1f%%', startangle=90)
            ax1.set_title('Распределение учителей по предметам')
        
        # Диаграмма по стажу
        if experience_ranges:
            ax2.bar(experience_ranges.keys(), experience_ranges.values(), 
                   color=['lightblue', 'lightgreen', 'lightcoral', 'gold'])
            ax2.set_title('Распределение учителей по стажу')
            ax2.set_ylabel('Количество учителей')
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_classrooms_stats(self):
        """Показать статистику классов"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Анализ данных классов
        grade_levels = {}
        student_counts = []
        
        for classroom in self.classroom_vm.classrooms:
            # По уровням классов
            if classroom.grade_level not in grade_levels:
                grade_levels[classroom.grade_level] = 0
            grade_levels[classroom.grade_level] += 1
            
            student_counts.append(classroom.student_count)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Диаграмма по уровням
        if grade_levels:
            levels = sorted(grade_levels.keys())
            counts = [grade_levels[level] for level in levels]
            ax1.bar([f"{level} класс" for level in levels], counts, color='lightblue')
            ax1.set_title('Распределение классов по уровням')
            ax1.set_ylabel('Количество классов')
        
        # Гистограмма по количеству учеников
        if student_counts:
            ax2.hist(student_counts, bins=8, color='lightgreen', edgecolor='black')
            ax2.set_title('Распределение классов по количеству учеников')
            ax2.set_xlabel('Количество учеников')
            ax2.set_ylabel('Количество классов')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_subjects_stats(self):
        """Показать распределение по предметам"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Анализ нагрузки учителей по предметам
        subject_load = {}
        
        for teacher in self.teacher_vm.teachers:
            if teacher.subject not in subject_load:
                subject_load[teacher.subject] = 0
            # Подсчитываем количество классов, которые ведет учитель
            classes_taught = sum(1 for classroom in self.classroom_vm.classrooms 
                               if classroom.teacher_id == teacher.id)
            subject_load[teacher.subject] += classes_taught
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if subject_load:
            subjects = list(subject_load.keys())
            load = list(subject_load.values())
            
            bars = ax.bar(subjects, load, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6'])
            ax.set_title('Нагрузка учителей по предметам (количество классов)')
            ax.set_ylabel('Количество классов')
            ax.set_xlabel('Предметы')
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            # Добавляем значения на столбцы
            for bar, value in zip(bars, load):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                       str(value), ha='center', va='bottom')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

def main():
    json_service = JSONService()
    teacher_vm = TeacherViewModel(json_service)
    classroom_vm = ClassroomViewModel(teacher_vm, json_service)

    app = CustomMainWindow(teacher_vm, classroom_vm)
    app.mainloop()

if __name__ == "__main__":
    main()