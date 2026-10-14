import os        # для очистки консоли в анимации (os.system)
import time      # для пауз между кадрами анимации
import math      # для вычисления квадратного корня в графике функции

RESET = "\033[0m"                       # сброс всех заданных ранее атрибутов

# Фоновые цвета в режиме TrueColor: \033[48;2;R;G;Bm
BG_WHITE = "\033[48;2;255;255;255m"     # белый фон  — верхняя полоса флага
BG_RED   = "\033[48;2;220;20;60m"       # красный (crimson #DC143C) — нижняя полоса
BG_BLACK = "\033[48;2;0;0;0m"           # чёрный фон — "чернила" узора

# Цвета текста (\033[38;2;R;G;Bm) для диаграммы и графика
FG_CYAN   = "\033[38;2;0;200;200m"
FG_YELLOW = "\033[38;2;230;180;40m"
FG_GREEN  = "\033[38;2;90;200;90m"
FG_GREY   = "\033[38;2;140;140;140m"
BOLD      = "\033[1m"


def title(text):
    """Печатает заголовок раздела, чтобы вывод не сливался в одну кашу."""
    print()
    print(BOLD + FG_CYAN + "=" * 60 + RESET)
    print(BOLD + FG_CYAN + "  " + text + RESET)
    print(BOLD + FG_CYAN + "=" * 60 + RESET)
    print()

#ФЛАГ ПОЛЬШИ

def draw_flag(height=10, width=32):
    half = height // 2                       # высота одной полосы

    for row in range(height):
        # Первая половина строк — белая, вторая — красная.
        color = BG_WHITE if row < half else BG_RED
        # Печатаем строку из пробелов на цветном фоне и обязательно сбрасываем
        # атрибуты в конце строки, иначе цвет "потечёт" до конца терминала.
        print(color + " " * width + RESET)

TILE_W = 12

def tile_rows():
    bar = "#" * TILE_W                            # сплошная горизонтальная полоса
    # Центральная перемычка: два символа ровно посередине плитки.
    center = [" "] * TILE_W
    center[TILE_W // 2 - 1] = "#"
    center[TILE_W // 2] = "#"
    center = "".join(center)
    # Две боковые перемычки: на 1/4 и 3/4 ширины плитки.
    sides = [" "] * TILE_W
    for pos in (TILE_W // 4 - 1, TILE_W // 4, TILE_W - TILE_W // 4 - 1, TILE_W - TILE_W // 4):
        sides[pos] = "#"
    sides = "".join(sides)
    return [bar, center, bar, sides]


def draw_pattern(repeat_x=4, repeat_y=2, use_color=True):
    rows = tile_rows()
    # Собираем все строки узора: repeat_y копий плитки + замыкающая полоса.
    all_rows = rows * repeat_y + [rows[0]]

    for mask in all_rows:
        line = mask * repeat_x               # размножаем плитку по горизонтали
        if use_color:
            # Переводим маску в цветную строку: '#' -> чёрный фон, ' ' -> сброс.
            out = ""
            for ch in line:
                out += (BG_BLACK + " " + RESET) if ch == "#" else " "
            print(out)
        else:
            print(line)

def draw_function(x_max=16, rows=10, cols=40):
    y_max = math.sqrt(x_max)                 # максимальное значение функции на отрезке

    # Пустое поле: список строк, каждая — список символов (чтобы можно было менять).
    field = [[" "] * cols for _ in range(rows)]

    for col in range(cols):
        # Переводим номер столбца в реальное значение x.
        x = x_max * col / (cols - 1)
        y = math.sqrt(x)                     # собственно функция варианта 4

        # Масштабируем y в номер строки снизу вверх.
        row_from_bottom = round(y / y_max * (rows - 1))
        row = rows - 1 - row_from_bottom     # переворачиваем: 0-я строка — верх экрана

        field[row][col] = "*"

    # --- вывод поля вместе с осями ---
    print(FG_GREY + "  y" + RESET)
    for r, line in enumerate(field):
        # Подписываем крайние значения оси Y.
        if r == 0:
            label = "{:4.1f}".format(y_max)
        elif r == rows - 1:
            label = " 0.0"
        else:
            label = "    "
        print(FG_GREY + label + " |" + RESET + FG_GREEN + "".join(line) + RESET)

    # Горизонтальная ось X с подписями.
    print(FG_GREY + "     +" + "-" * cols + "> x" + RESET)
    print(FG_GREY + "      0" + " " * (cols - 4) + "{:<4}".format(x_max) + RESET)

def read_sequence(path="sequence.txt"):
    """
    Читает файл с числовой последовательностью (по одному числу в строке).
    Возвращает список чисел типа float.
    """
    numbers = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()              # убираем пробелы и перевод строки
            if line:                         # пустые строки игнорируем
                numbers.append(float(line))
    return numbers


def draw_diagram(numbers, bar_width=50):
    half = 125                               # размер половины по условию

    first = numbers[:half]                   # первые 125 чисел
    second = numbers[half:half * 2]          # вторые 125 чисел

    # Среднее арифметическое модулей значений.
    avg_first = sum(abs(x) for x in first) / len(first)
    avg_second = sum(abs(x) for x in second) / len(second)

    total = avg_first + avg_second           # база для перевода в проценты
    pct_first = avg_first / total * 100
    pct_second = avg_second / total * 100

    # Длина полоски пропорциональна проценту.
    len_first = round(bar_width * pct_first / 100)
    len_second = bar_width - len_first       # чтобы в сумме всегда было bar_width

    print("  Среднее по модулю, числа 1-125  : {:.4f}".format(avg_first))
    print("  Среднее по модулю, числа 126-250: {:.4f}".format(avg_second))
    print()
    print("  Процентное соотношение:")
    print()
    print("  1-125   " + FG_CYAN + "█" * len_first + RESET +
          FG_GREY + "·" * (bar_width - len_first) + RESET +
          "  {:5.2f}%".format(pct_first))
    print("  126-250 " + FG_YELLOW + "█" * len_second + RESET +
          FG_GREY + "·" * (bar_width - len_second) + RESET +
          "  {:5.2f}%".format(pct_second))

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def flag_frame(phase, height=10, width=36):
    half = height / 2
    lines = []

    for row in range(height):
        line = ""
        for col in range(width):
            # Волна: граница между белым и красным колеблется по оси X.
            offset = math.sin(col / 5.0 + phase) * 1.5
            color = BG_WHITE if row < half + offset else BG_RED
            line += color + " "
        lines.append(line + RESET)

    return lines


def animate(frames=3, loops=4, delay=0.25):
    for loop in range(loops):
        for i in range(frames):
            clear_screen()                   # стираем предыдущий кадр
            phase = 2 * math.pi * i / frames # равномерно распределяем фазу по кадрам
            print(BOLD + FG_CYAN + "  Допзадание: анимация (Ctrl+C — выход)" + RESET)
            print()
            for line in flag_frame(phase):
                print(line)
            time.sleep(delay)                # ждём перед следующим кадром

    clear_screen()


def main():
    """Последовательно выполняет все четыре пункта задания и допзадание."""

    title("1. Флаг Польши")
    draw_flag()

    title("2. Узор (вариант d)")
    draw_pattern(repeat_x=4, repeat_y=2)

    title("3. График функции y = x^0.5")
    draw_function()

    title("4. Диаграмма по sequence.txt")
    try:
        numbers = read_sequence("sequence.txt")
        draw_diagram(numbers)
    except FileNotFoundError:
        # Если файла рядом нет — сообщаем об этом, а не падаем с трассировкой.
        print("  Файл sequence.txt не найден — положите его рядом с main.py")

    title("5. Допзадание: анимация")
    print("  Нажмите Enter для запуска анимации (или Ctrl+C для выхода)...")
    try:
        input()
        animate()
        print("Анимация завершена.")
    except (KeyboardInterrupt, EOFError):
        print("\nАнимация пропущена.")

if __name__ == "__main__":
    main()
