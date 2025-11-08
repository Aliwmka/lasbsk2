class Teacher:
    """Класс, представляющий учителя."""

    def __init__(self, id: int, full_name: str, subject: str, experience: int, category: str, phone: str = ""):
        self.id = id
        self.full_name = full_name
        self.subject = subject
        self.experience = experience
        self.category = category
        self.phone = phone

    def to_dict(self):
        """Преобразование объекта в словарь для JSON"""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "subject": self.subject,
            "experience": self.experience,
            "category": self.category,
            "phone": self.phone
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря"""
        return cls(
            id=data["id"],
            full_name=data["full_name"],
            subject=data["subject"],
            experience=data["experience"],
            category=data["category"],
            phone=data["phone"]
        )

    def __repr__(self):
        return f"Teacher(id={self.id}, full_name='{self.full_name}', subject='{self.subject}', experience={self.experience}, category='{self.category}', phone='{self.phone}')"