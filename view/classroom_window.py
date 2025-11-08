import tkinter as tk
from tkinter import ttk, messagebox
from view.new_classroom_window import NewClassroomWindow

class ClassroomWindow(tk.Toplevel):
    def __init__(self, parent, classroom_vm, teacher_vm):
        super().__init__(parent)
        self.title("Классы")
        self.geometry("800x450")
        self.classroom_vm = classroom_vm
        self.teacher_vm = teacher_vm
        self.classroom_vm.set_on_data_changed(self.refresh_table)

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Добавить", command=self.add_classroom).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_classroom).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_classroom).pack(side="left", padx=5)

        # Таблица
        columns = ("ID", "Класс", "Классный руководитель", "Кол-во учеников", "Уровень")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("ID", width=50)
        self.tree.column("Класс", width=80)
        self.tree.column("Классный руководитель", width=200)
        self.tree.column("Кол-во учеников", width=120)
        self.tree.column("Уровень", width=80)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def refresh_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Создаём словарь ID → ФИО учителя
        teacher_map = {teacher.id: teacher.full_name for teacher in self.teacher_vm.teachers}
        
        # Заполнение
        for classroom in self.classroom_vm.classrooms:
            teacher_name = teacher_map.get(classroom.teacher_id, "Неизвестно")
            self.tree.insert("", "end", values=(
                classroom.id, classroom.class_name, teacher_name, 
                classroom.student_count, classroom.grade_level
            ))

    def get_selected_id(self):
        sel = self.tree.selection()
        return int(self.tree.item(sel[0])["values"][0]) if sel else None

    def add_classroom(self):
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
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def edit_classroom(self):
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
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_classroom(self):
        classroom_id = self.get_selected_id()
        if not classroom_id:
            messagebox.showwarning("Внимание", "Выберите класс для удаления.")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить класс?"):
            try:
                self.classroom_vm.delete_classroom(classroom_id)
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))