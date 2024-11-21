import struct
import yaml
import sys


def instruction_to_bytes(instruction):
    """Преобразование инструкции в массив байтов (7 байт)."""
    raw_bytes = struct.pack("<Q", instruction)[:7]
    return [f"0x{b:02X}" for b in raw_bytes]

def extract_signed_field(instruction, shift, bit_length):
    # Маска для извлечения нужного поля
    mask = (1 << bit_length) - 1
    # Извлечение значения поля
    value = (instruction >> shift) & mask

    # Проверка на отрицательность (если старший бит равен 1)
    if value & (1 << (bit_length - 1)):
        # Если старший бит равен 1, значит число отрицательное
        value -= (1 << bit_length)

    return value


def interpret(binary_file, result_file, memory_range):
    with open(binary_file, "rb") as f:
        data = f.read()

    memory = [0] * 1024  # Простая модель памяти
    program_counter = 0
    log_data = []

    while program_counter < len(data):
        # Читаем инструкцию
        instruction = int.from_bytes(data[program_counter:program_counter + 7], "little")
        program_counter += 7

        # Распаковка команды с учетом знаков
        A = instruction & 0x1F  # Первые 5 бит для A
        B = extract_signed_field(instruction, 5, 14)  # Извлекаем знаковое поле B
        C = extract_signed_field(instruction, 19, 14)  # Извлекаем знаковое поле C
        D = instruction >> 33  # Поле D всегда без знака, так как оно всегда занимает 6 бит

        # Выполнение команды
        if A == 19:  # LOAD_CONST
            memory[B] = C
        elif A == 22:  # READ_MEM
            memory[C] = memory[memory[B]]
        elif A == 24:  # WRITE_MEM
            memory[B] = memory[C]
        elif A == 23:  # UNARY_ABS
            # Индекс для вычисления
            index = memory[C] + D
            memory[B] = abs(index)
            

        # Логируем данные
        log_data.append({
            "bytes": instruction_to_bytes(instruction),  # Вывод в формате байтов
            "A": A,
            "B": B,
            "C": C,
            "D": D if A == 23 else None,
            "memory_snapshot": memory[:10],  # Частичная память для отладки
        })

    # Сохраняем результат в диапазоне памяти
    result = {"memory": memory[memory_range[0]:memory_range[1]], "log": log_data}
    with open(result_file, "w") as f:
        yaml.dump(result, f, default_flow_style=False)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python interpreter.py <binary_file> <result_file> <range_start> <range_end>")
        sys.exit(1)

    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    range_start = int(sys.argv[3])
    range_end = int(sys.argv[4])
    interpret(binary_file, result_file, (range_start, range_end))
