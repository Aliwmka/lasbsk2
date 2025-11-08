import tkinter as tk
from tkinter import ttk, messagebox

class NewTeacherWindow(tk.Toplevel):
    """Диалоговое окно для добавления или редактирования учителя."""
    
    def __init__(self, parent, teacher_id=None, full_name="", subject="", experience=0, category="", phone=""):
        super().__init__(parent)
        self.title("Новый учитель" if teacher_id is None else "Редактировать учителя")
        self.geometry("450x350")
        self.grab_set()  # Модальное окно

        self.result = None

        # Поле ID (только для чтения)
        tk.Label(self, text="ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.id_var = tk.StringVar()
        self.id_var.set(str(teacher_id) if teacher_id else "")
        tk.Entry(self, textvariable=self.id_var, state="readonly", width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Поле ФИО
        tk.Label(self, text="ФИО:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.name_var = tk.StringVar(value=full_name)
        tk.Entry(self, textvariable=self.name_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        # Поле Предмет
        tk.Label(self, text="Предмет:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.subject_var = tk.StringVar(value=subject)
        subject_combobox = ttk.Combobox(self, textvariable=self.subject_var, 
                                      values=["Математика", "Физика", "Химия", "Биология", "История", 
                                             "Литература", "Русский язык", "Иностранный язык", 
                                             "География", "Информатика", "Физкультура", "Музыка", "ИЗО"],
                                      state="readonly", width=27)
        subject_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Поле Стаж
        tk.Label(self, text="Стаж (лет):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.experience_var = tk.StringVar(value=str(experience))
        tk.Entry(self, textvariable=self.experience_var, width=10).grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Поле Категория
        tk.Label(self, text="Категория:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.category_var = tk.StringVar(value=category)
        category_combobox = ttk.Combobox(self, textvariable=self.category_var, 
                                       values=["Высшая", "Первая", "Вторая", "Без категории"],
                                       state="readonly", width=27)
        category_combobox.grid(row=4, column=1, padx=5, pady=5)

        # Поле Телефон
        tk.Label(self, text="Телефон:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.phone_var = tk.StringVar(value=phone)
        tk.Entry(self, textvariable=self.phone_var, width=30).grid(row=5, column=1, padx=5, pady=5)

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Сохранить", command=self.save).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Отменить", command=self.destroy).pack(side="left", padx=5)

    def validate(self):
        """Проверка введённых данных."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "ФИО не может быть пустым!")
            return False

        subject = self.subject_var.get().strip()
        if not subject:
            messagebox.showerror("Ошибка", "Предмет не может быть пустым!")
            return False

        try:
            experience = int(self.experience_var.get())
            if experience < 0 or experience > 50:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Стаж должен быть числом от 0 до 50!")
            return False

        category = self.category_var.get().strip()
        if not category:
            messagebox.showerror("Ошибка", "Категория не может быть пустой!")
            return False

        return True

    def save(self):
        """Сохранение данных."""
        if not self.validate():
            return

        try:
            teacher_id = int(self.id_var.get()) if self.id_var.get() else None
        except ValueError:
            teacher_id = None

        self.result = {
            "id": teacher_id,
            "full_name": self.name_var.get().strip(),
            "subject": self.subject_var.get().strip(),
            "experience": int(self.experience_var.get()),
            "category": self.category_var.get().strip(),
            "phone": self.phone_var.get().strip()
        }
        self.destroy()