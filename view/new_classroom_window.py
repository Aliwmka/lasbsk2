import tkinter as tk
from tkinter import ttk, messagebox

class NewClassroomWindow(tk.Toplevel):
    """Диалоговое окно для добавления или редактирования класса."""
    
    def __init__(self, parent, teachers, classroom_id=None, class_name="", teacher_id=None, student_count=0, grade_level=1):
        super().__init__(parent)
        self.title("Новый класс" if classroom_id is None else "Редактировать класс")
        self.geometry("450x300")
        self.grab_set()  # Модальное окно

        self.result = None
        self.teachers = teachers

        # Поле ID (только для чтения)
        tk.Label(self, text="ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.id_var = tk.StringVar()
        self.id_var.set(str(classroom_id) if classroom_id else "")
        tk.Entry(self, textvariable=self.id_var, state="readonly", width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Поле Название класса
        tk.Label(self, text="Название класса:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.name_var = tk.StringVar(value=class_name)
        tk.Entry(self, textvariable=self.name_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        # Выбор классного руководителя
        tk.Label(self, text="Классный руководитель:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.teacher_var = tk.StringVar()
        teacher_names = [f"{teacher.full_name} ({teacher.subject})" for teacher in self.teachers]
        self.teacher_combobox = ttk.Combobox(self, textvariable=self.teacher_var, values=teacher_names, state="readonly", width=27)
        self.teacher_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Установка выбранного учителя
        if teacher_id is not None:
            teacher_ids = [teacher.id for teacher in self.teachers]
            try:
                idx = teacher_ids.index(teacher_id)
                self.teacher_combobox.current(idx)
            except ValueError:
                pass

        # Поле Количество учеников
        tk.Label(self, text="Кол-во учеников:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.students_var = tk.StringVar(value=str(student_count))
        tk.Entry(self, textvariable=self.students_var, width=10).grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Поле Уровень класса
        tk.Label(self, text="Уровень класса:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.grade_var = tk.IntVar(value=grade_level)
        grade_frame = tk.Frame(self)
        grade_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        grade_combobox = ttk.Combobox(grade_frame, textvariable=self.grade_var, 
                                    values=list(range(1, 12)), state="readonly", width=5)
        grade_combobox.pack(side="left")
        tk.Label(grade_frame, text="класс").pack(side="left", padx=(5, 0))

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Сохранить", command=self.save).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Отменить", command=self.destroy).pack(side="left", padx=5)

    def validate(self):
        """Проверка введённых данных."""
        class_name = self.name_var.get().strip()
        if not class_name:
            messagebox.showerror("Ошибка", "Название класса не может быть пустым!")
            return False

        if not self.teacher_var.get():
            messagebox.showerror("Ошибка", "Выберите классного руководителя!")
            return False

        try:
            student_count = int(self.students_var.get())
            if student_count < 1 or student_count > 40:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество учеников должно быть числом от 1 до 40!")
            return False

        grade_level = self.grade_var.get()
        if grade_level < 1 or grade_level > 11:
            messagebox.showerror("Ошибка", "Уровень класса должен быть от 1 до 11!")
            return False

        return True

    def save(self):
        """Сохранение данных."""
        if not self.validate():
            return

        # Получаем ID выбранного учителя
        selected_teacher_name = self.teacher_var.get()
        teacher_ids = [teacher.id for teacher in self.teachers]
        teacher_names = [f"{teacher.full_name} ({teacher.subject})" for teacher in self.teachers]
        teacher_id = teacher_ids[teacher_names.index(selected_teacher_name)]

        try:
            classroom_id = int(self.id_var.get()) if self.id_var.get() else None
        except ValueError:
            classroom_id = None

        self.result = {
            "id": classroom_id,
            "class_name": self.name_var.get().strip(),
            "teacher_id": teacher_id,
            "student_count": int(self.students_var.get()),
            "grade_level": self.grade_var.get()
        }
        self.destroy()