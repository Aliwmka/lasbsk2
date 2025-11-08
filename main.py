from view.main_window import MainWindow
from viewmodel.teacher_viewmodel import TeacherViewModel
from viewmodel.classroom_viewmodel import ClassroomViewModel
from service.json_service import JSONService

def main():
    # Создание сервиса для работы с JSON
    json_service = JSONService()

    # Создание ViewModel с передачей JSON сервиса
    teacher_vm = TeacherViewModel(json_service)
    classroom_vm = ClassroomViewModel(teacher_vm, json_service)

    # Глобальные переменные для доступа между ViewModel
    import builtins
    builtins.teacher_vm = teacher_vm
    builtins.classroom_vm = classroom_vm

    # Запуск приложения
    app = MainWindow(teacher_vm, classroom_vm)
    app.mainloop()

if __name__ == "__main__":
    main()