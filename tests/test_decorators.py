from datetime import datetime

from src.decorators import log


def test_log_to_file(tmp_path):
    """
    Тестирование записи логов в файл при успешном выполнении функции
    """
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def add(a, b):
        return a + b

    result = add(2, 3)

    # Проверяем результат выполнения
    assert result == 5

    # Проверяем содержимое лог-файла
    with open(log_file, "r") as f:
        content = f.read()
        assert "add ok" in content
        assert datetime.now().strftime("%Y-%m-%d") in content


def test_log_to_console(capsys):
    """
    Тестирование вывода логов в консоль при успешном выполнении
    """

    @log()
    def multiply(a, b):
        return a * b

    result = multiply(3, 4)

    # Проверяем результат
    assert result == 12

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()
    assert "multiply ok" in captured.out
    assert datetime.now().strftime("%Y-%m-%d") in captured.out


def test_log_error_to_file(tmp_path):
    """
    Тестирование записи ошибок в файл
    """
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b

    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass

    # Проверяем содержимое лог-файла
    with open(log_file, "r") as f:
        content = f.read()
        assert "divide error: ZeroDivisionError" in content
        assert "Inputs: (10, 0), {}" in content
        assert datetime.now().strftime("%Y-%m-%d") in content


def test_log_error_to_console(capsys):
    """
    Тестирование вывода ошибок в консоль
    """

    @log()
    def subtract(a, b):
        if a < b:
            raise ValueError("a must be greater than b")
        return a - b

    try:
        subtract(1, 5)
    except ValueError:
        pass

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()
    assert "subtract error: ValueError" in captured.out
    assert "Inputs: (1, 5), {}" in captured.out
    assert datetime.now().strftime("%Y-%m-%d") in captured.out


def test_log_with_kwargs(tmp_path):
    log_file = tmp_path / "kwargs.log"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b  # Эта функция вызовет ошибку при b=0

    # Успешный вызов
    assert divide(10, 2) == 5

    # Вызов с ошибкой
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass

    # Проверяем логи
    with open(log_file, "r") as f:
        content = f.read()
        assert "divide ok" in content
        assert "divide error: ZeroDivisionError" in content


def test_function_metadata_preserved():
    """
    Тестирование сохранения метаданных функции
    """

    @log()
    def example(a: int, b: int = 1) -> int:
        """Example function"""
        return a + b

    assert example.__name__ == "example"
    assert example.__doc__ == "Example function"
    assert example.__annotations__ == {"a": int, "b": int, "return": int}


def test_empty_filename_uses_console(capsys):
    """
    Тестирование поведения при пустом имени файла
    """

    @log(filename="")
    def test_func():
        return "test"

    test_func()
    captured = capsys.readouterr()
    assert "test_func ok" in captured.out
