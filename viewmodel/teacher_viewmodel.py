from typing import List, Callable
from model.teacher import Teacher
from service.json_service import JSONService

class TeacherViewModel:
    def __init__(self, json_service: JSONService):
        self.json_service = json_service
        # Загрузка данных из JSON при инициализации
        self._teachers: List[Teacher] = self.json_service.load_data("teachers.json", Teacher)
        self._on_data_changed: Callable[[], None] = None

    @property
    def teachers(self) -> List[Teacher]:
        return self._teachers

    def set_on_data_changed(self, callback: Callable[[], None]):
        self._on_data_changed = callback

    def _notify(self):
        if self._on_data_changed:
            self._on_data_changed()

    def _save_data(self):
        """Сохранение данных в JSON файл"""
        self.json_service.save_data("teachers.json", self._teachers)

    def add_teacher(self, full_name: str, subject: str, experience: int, category: str, phone: str = ""):
        if not full_name.strip():
            raise ValueError("ФИО не может быть пустым.")

        if not subject.strip():
            raise ValueError("Предмет не может быть пустым.")

        if experience < 0 or experience > 50:
            raise ValueError("Стаж должен быть от 0 до 50 лет.")

        if not category.strip():
            raise ValueError("Категория не может быть пустой.")

        # Проверка на уникальность ФИО
        if any(t.full_name.lower() == full_name.strip().lower() for t in self._teachers):
            raise ValueError("Учитель с таким ФИО уже существует.")

        # Генерация нового ID
        new_id = max((t.id for t in self._teachers), default=0) + 1
        new_teacher = Teacher(new_id, full_name.strip(), subject.strip(), experience, category.strip(), phone.strip())
        self._teachers.append(new_teacher)
        self._save_data()
        self._notify()

    def update_teacher(self, teacher_id: int, full_name: str, subject: str, experience: int, category: str, phone: str):
        if not full_name.strip():
            raise ValueError("ФИО не может быть пустым.")

        if not subject.strip():
            raise ValueError("Предмет не может быть пустым.")

        if experience < 0 or experience > 50:
            raise ValueError("Стаж должен быть от 0 до 50 лет.")

        if not category.strip():
            raise ValueError("Категория не может быть пустой.")

        # Проверка на уникальность ФИО (исключая текущего учителя)
        if any(t.full_name.lower() == full_name.strip().lower() and 
               t.id != teacher_id for t in self._teachers):
            raise ValueError("Учитель с таким ФИО уже существует.")

        for teacher in self._teachers:
            if teacher.id == teacher_id:
                teacher.full_name = full_name.strip()
                teacher.subject = subject.strip()
                teacher.experience = experience
                teacher.category = category.strip()
                teacher.phone = phone.strip()
                self._save_data()
                self._notify()
                return
        raise ValueError(f"Учитель с ID {teacher_id} не найден.")

    def delete_teacher(self, teacher_id: int):
        # Проверяем, является ли учитель классным руководителем
        from main import classroom_vm
        teacher_classrooms = [c for c in classroom_vm.classrooms if c.teacher_id == teacher_id]
        if teacher_classrooms:
            classroom_names = ", ".join([c.class_name for c in teacher_classrooms])
            raise ValueError(f"Нельзя удалить учителя, который является классным руководителем классов: {classroom_names}")

        self._teachers = [t for t in self._teachers if t.id != teacher_id]
        self._save_data()
        self._notify()

    def get_teacher_by_id(self, teacher_id: int) -> Teacher:
        for teacher in self._teachers:
            if teacher.id == teacher_id:
                return teacher
        raise ValueError(f"Учитель с ID {teacher_id} не найден.")