from typing import List, Callable
from model.classroom import Classroom
from service.json_service import JSONService

class ClassroomViewModel:
    def __init__(self, teacher_vm, json_service: JSONService):
        self.teacher_vm = teacher_vm
        self.json_service = json_service
        # Загрузка данных из JSON при инициализации
        self._classrooms: List[Classroom] = self.json_service.load_data("classrooms.json", Classroom)
        self._on_data_changed: Callable[[], None] = None

    @property
    def classrooms(self) -> List[Classroom]:
        return self._classrooms

    def set_on_data_changed(self, callback: Callable[[], None]):
        self._on_data_changed = callback

    def _notify(self):
        if self._on_data_changed:
            self._on_data_changed()

    def _save_data(self):
        """Сохранение данных в JSON файл"""
        self.json_service.save_data("classrooms.json", self._classrooms)

    def add_classroom(self, class_name: str, teacher_id: int, student_count: int, grade_level: int):
        if not class_name.strip():
            raise ValueError("Название класса не может быть пустым.")

        if student_count < 1 or student_count > 40:
            raise ValueError("Количество учеников должно быть от 1 до 40.")

        if grade_level < 1 or grade_level > 11:
            raise ValueError("Уровень класса должен быть от 1 до 11.")

        # Проверяем существование учителя
        teacher_exists = any(t.id == teacher_id for t in self.teacher_vm.teachers)
        if not teacher_exists:
            raise ValueError("Указанный учитель не существует.")

        # Проверка на уникальность названия класса
        if any(c.class_name.lower() == class_name.strip().lower() for c in self._classrooms):
            raise ValueError("Класс с таким названием уже существует.")

        # Генерация нового ID
        new_id = max((c.id for c in self._classrooms), default=0) + 1
        new_classroom = Classroom(new_id, class_name.strip(), teacher_id, student_count, grade_level)
        self._classrooms.append(new_classroom)
        self._save_data()
        self._notify()

    def update_classroom(self, classroom_id: int, class_name: str, teacher_id: int, student_count: int, grade_level: int):
        if not class_name.strip():
            raise ValueError("Название класса не может быть пустым.")

        if student_count < 1 or student_count > 40:
            raise ValueError("Количество учеников должно быть от 1 до 40.")

        if grade_level < 1 or grade_level > 11:
            raise ValueError("Уровень класса должен быть от 1 до 11.")

        # Проверяем существование учителя
        teacher_exists = any(t.id == teacher_id for t in self.teacher_vm.teachers)
        if not teacher_exists:
            raise ValueError("Указанный учитель не существует.")

        # Проверка на уникальность названия класса (исключая текущий класс)
        if any(c.class_name.lower() == class_name.strip().lower() and 
               c.id != classroom_id for c in self._classrooms):
            raise ValueError("Класс с таким названием уже существует.")

        for classroom in self._classrooms:
            if classroom.id == classroom_id:
                classroom.class_name = class_name.strip()
                classroom.teacher_id = teacher_id
                classroom.student_count = student_count
                classroom.grade_level = grade_level
                self._save_data()
                self._notify()
                return
        raise ValueError(f"Класс с ID {classroom_id} не найден.")

    def delete_classroom(self, classroom_id: int):
        self._classrooms = [c for c in self._classrooms if c.id != classroom_id]
        self._save_data()
        self._notify()

    def get_classroom_by_id(self, classroom_id: int) -> Classroom:
        for classroom in self._classrooms:
            if classroom.id == classroom_id:
                return classroom
        raise ValueError(f"Класс с ID {classroom_id} не найден.")