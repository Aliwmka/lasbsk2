class Classroom:
    """Класс, представляющий учебный класс."""

    def __init__(self, id: int, class_name: str, teacher_id: int, student_count: int, grade_level: int):
        self.id = id
        self.class_name = class_name
        self.teacher_id = teacher_id
        self.student_count = student_count
        self.grade_level = grade_level

    def to_dict(self):
        """Преобразование объекта в словарь для JSON"""
        return {
            "id": self.id,
            "class_name": self.class_name,
            "teacher_id": self.teacher_id,
            "student_count": self.student_count,
            "grade_level": self.grade_level
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря"""
        return cls(
            id=data["id"],
            class_name=data["class_name"],
            teacher_id=data["teacher_id"],
            student_count=data["student_count"],
            grade_level=data["grade_level"]
        )

    def __repr__(self):
        return f"Classroom(id={self.id}, class_name='{self.class_name}', teacher_id={self.teacher_id}, students={self.student_count}, grade={self.grade_level})"