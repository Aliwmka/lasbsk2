import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self, teacher_vm, classroom_vm):
        super().__init__()
        self.title("Школьная система управления")
        self.geometry("1000x600")
        self.teacher_vm = teacher_vm
        self.classroom_vm = classroom_vm

        self.create_menu()
        self.create_main_content()
        self.refresh_data()

    def create_menu(self):
        """Создание простого меню"""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # Меню "Управление"
        manage_menu = tk.Menu(menu_bar, tearoff=0)
        manage_menu.add_command(label="Управление учителями", 
                               command=lambda: self.open_teachers(self.teacher_vm))
        manage_menu.add_command(label="Управление классами", 
                               command=lambda: self.open_classrooms(self.classroom_vm, self.teacher_vm))
        menu_bar.add_cascade(label="Управление", menu=manage_menu)

    def create_main_content(self):
        """Создание основного содержимого"""
        # Заголовок
        title_label = tk.Label(self, text="🏫 ШКОЛЬНАЯ СИСТЕМА УПРАВЛЕНИЯ", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Статистика
        self.stats_label = tk.Label(self, text="", font=("Arial", 10))
        self.stats_label.pack(pady=5)

        # Таблица всех классов
        self.create_classrooms_table()

    def create_classrooms_table(self):
        """Создание таблицы со всеми классами"""
        # Таблица
        columns = ("ID", "Класс", "Классный руководитель", "Предмет", "Кол-во учеников", "Уровень")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)

        # Настройка колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("Класс", text="Класс")
        self.tree.heading("Классный руководитель", text="Классный руководитель")
        self.tree.heading("Предмет", text="Предмет")
        self.tree.heading("Кол-во учеников", text="Кол-во учеников")
        self.tree.heading("Уровень", text="Уровень")

        self.tree.column("ID", width=50)
        self.tree.column("Класс", width=80)
        self.tree.column("Классный руководитель", width=200)
        self.tree.column("Предмет", width=120)
        self.tree.column("Кол-во учеников", width=120)
        self.tree.column("Уровень", width=80)

        # Скроллбар
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def refresh_data(self):
        """Обновление данных в таблице"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Обновление статистики
        total_teachers = len(self.teacher_vm.teachers)
        total_classrooms = len(self.classroom_vm.classrooms)
        total_students = sum(classroom.student_count for classroom in self.classroom_vm.classrooms)
        
        self.stats_label.config(
            text=f"Учителей: {total_teachers} | Классов: {total_classrooms} | Учеников: {total_students}"
        )

        # Создаём словарь ID → учитель
        teacher_map = {teacher.id: teacher for teacher in self.teacher_vm.teachers}
        
        # Заполнение таблицы классами
        for classroom in self.classroom_vm.classrooms:
            teacher = teacher_map.get(classroom.teacher_id)
            teacher_name = teacher.full_name if teacher else "Неизвестно"
            teacher_subject = teacher.subject if teacher else "Неизвестно"
            
            self.tree.insert("", "end", values=(
                classroom.id, 
                classroom.class_name,
                teacher_name,
                teacher_subject,
                classroom.student_count, 
                f"{classroom.grade_level} класс"
            ))

    def open_teachers(self, vm):
        """Открытие окна управления учителями"""
        from view.teacher_window import TeacherWindow
        window = TeacherWindow(self, vm)
        self.wait_window(window)
        self.refresh_data()

    def open_classrooms(self, classroom_vm, teacher_vm):
        """Открытие окна управления классами"""
        from view.classroom_window import ClassroomWindow
        window = ClassroomWindow(self, classroom_vm, teacher_vm)
        self.wait_window(window)
        self.refresh_data()