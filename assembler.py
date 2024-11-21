import struct
import yaml
import sys


COMMANDS = {
    "LOAD_CONST": 19,
    "READ_MEM": 22,
    "WRITE_MEM": 24,
    "UNARY_ABS": 23,
}


def instruction_to_bytes(instruction):
    """Преобразование инструкции в массив байтов (7 байт)."""
    raw_bytes = struct.pack("<Q", instruction)[:7]
    return [f"0x{b:02X}" for b in raw_bytes]


def assemble(input_file, output_file, log_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    binary_data = bytearray()
    log_data = []

    for line in lines:
        parts = line.strip().split()
        command = parts[0]
        A = COMMANDS[command]
        B = int(parts[1])
        C = int(parts[2])
        D = int(parts[3]) if command == "UNARY_ABS" else 0

        # Формируем машинный код команды
        if command == "UNARY_ABS":
            instruction = (A & 0x1F) | ((B & 0x3FFF) << 5) | ((C & 0x3FFF) << 19) | ((D & 0x3F) << 33)
        else:
            instruction = (A & 0x1F) | ((B & 0x3FFF) << 5) | ((C & (0x3FFF if A != 19 else 0x1FFFFFFF)) << 19)

        # Сохраняем бинарное представление
        binary_data.extend(struct.pack("<Q", instruction)[:7])

        # Логируем данные
        log_data.append({
            "command": command,
            "A": A,
            "B": B,
            "C": C,
            "D": D if command == "UNARY_ABS" else None,
            "bytes": instruction_to_bytes(instruction)  # Вывод в формате байтов
        })

    # Сохраняем бинарный файл
    with open(output_file, "wb") as f:
        f.write(binary_data)

    # Сохраняем лог-файл
    with open(log_file, "w") as f:
        yaml.dump(log_data, f, default_flow_style=False)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
