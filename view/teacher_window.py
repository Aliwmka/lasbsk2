import tkinter as tk
from tkinter import ttk, messagebox
from view.new_teacher_window import NewTeacherWindow

class TeacherWindow(tk.Toplevel):
    def __init__(self, parent, view_model):
        super().__init__(parent)
        self.title("Учителя")
        self.geometry("900x450")
        self.vm = view_model
        self.vm.set_on_data_changed(self.refresh_table)

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Добавить", command=self.add_teacher).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_teacher).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_teacher).pack(side="left", padx=5)

        # Таблица
        columns = ("ID", "ФИО", "Предмет", "Стаж", "Категория", "Телефон")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("ID", width=50)
        self.tree.column("ФИО", width=200)
        self.tree.column("Предмет", width=120)
        self.tree.column("Стаж", width=80)
        self.tree.column("Категория", width=100)
        self.tree.column("Телефон", width=150)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def refresh_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Заполнение
        for teacher in self.vm.teachers:
            self.tree.insert("", "end", values=(
                teacher.id, teacher.full_name, teacher.subject, 
                f"{teacher.experience} лет", teacher.category, teacher.phone
            ))

    def get_selected_id(self):
        sel = self.tree.selection()
        return int(self.tree.item(sel[0])["values"][0]) if sel else None

    def add_teacher(self):
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
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def edit_teacher(self):
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
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_teacher(self):
        teacher_id = self.get_selected_id()
        if not teacher_id:
            messagebox.showwarning("Внимание", "Выберите учителя для удаления.")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить учителя?"):
            try:
                self.vm.delete_teacher(teacher_id)
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))