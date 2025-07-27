from datetime import datetime
from typing import Callable, Any, Optional
import functools



def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Параметры:
        filename: Имя файла для записи логов. Если None - вывод в консоль.

    Возвращает:
        Декорированную функцию с логированием
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Подготовка информации о вызове
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"{timestamp} - {func_name}"

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное выполнение
                success_message = f"{log_message} ok\n"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(success_message)
                else:
                    print(success_message, end="")

                return result

            except Exception as e:
                # Логируем ошибку
                error_message = f"{log_message} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}\n"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="")
                raise  # Пробрасываем исключение дальше

        return wrapper

    return decorator


@log(filename="operations.log")
def add(a: int, b: int) -> int:
    """Складывает два числа"""
    return a + b


@log()  # Логирование в консоль
def divide(a: int, b: int) -> float:
    """Делит первое число на второе"""
    return a / b


# Тестирование
if __name__ == "__main__":
    add(1, 2)  # Запишет в operations.log
    divide(4, 2)  # Выведет в консоль
    try:
        divide(4, 0)  # Выведет ошибку в консоль
    except ZeroDivisionError:
        pass
