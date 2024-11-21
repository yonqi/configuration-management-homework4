# configuration-management-homework4
Домашки по конфигурационному управлению (номер 4!)
## Вариант 10
### Задание 4

Разработать ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Система команд УВМ представлена далее.

Для ассемблера необходимо разработать читаемое представление команд УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к которой задается из командной строки. Результатом работы ассемблера является бинарный файл в виде последовательности байт, путь к которому задается из командной строки. Дополнительный ключ командной строки задает путь к файлулогу, в котором хранятся ассемблированные инструкции в духе списков “ключ=значение”, как в приведенных далее тестах.
 
Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон также указывается из командной строки.

Форматом для файла-лога и файла-результата является **yaml**.

Необходимо реализовать приведенные тесты для всех команд, а такженаписать и отладить тестовую программу.
 
**Операции:**
```
- Загрузка константы 
- Чтение из памяти 
- Запись в память 
- Унарная операция: abs()
```

**Тестовая программа**
```
Выполнить поэлементно операцию abs() над вектором длины 5. Результат записать в исходный вектор.
```

#### Общее описание проекта

Проект представляет собой ассемблер и интерпретатор для выполнения инструкций низкого уровня.

1. Ассемблер:

    - Читает входные текстовые команды из файла, преобразует их в двоичные инструкции и сохраняет в выходной файл.
    - Создает лог-файл, содержащий информацию о каждой инструкции и ее представление в байтах.

2. Интерпретатор:

    - Читает двоичные инструкции из файла, выполняет их и обновляет состояние памяти.
    - Логирует выполнение каждой инструкции, включая состояние памяти.

#### Описание функций

**Ассемблер**

1. `instruction_to_bytes`

  - Описание: преобразует 64-битное значение инструкции в массив из 7 байт.
  - Аргументы: instruction (int): Число, представляющее машинный код команды.
  - Возвращает: Список строк в формате 0xXX, представляющих байты инструкции.

2. `assemble`

  - Описание: считывает текстовые инструкции из файла, преобразует их в двоичный код, сохраняет в файл и генерирует лог.
  - Аргументы:
    - input_file (str): Имя входного файла с текстовыми командами.
    - output_file (str): Имя выходного файла для бинарных данных.
    - log_file (str): Имя выходного лог-файла.
  - Возвращает: Нет.

3. `main (встроенная)`

  - Описание: Проверяет аргументыОписаниеassemble.
  - Аргументы: Принимает аргументы командной строки.
  - Возвращает: Нет.
    
**Интерпретатор**

1. `instruction_to_bytes`

  - Описание: аналогичная функция из ассемблера, используется для регистрации инструкций.
  - Аргументы: instruction (int): Число, представляющее машинный код команды.
  - Возвращает: Список строк в формате 0xXX.

2. `extract_signed_field`

  - Описание: извлекает знаковое значение из инструкции, используя битовую маску.
  - Аргументы:
    - instruction (int): Число, представляющее машинный код команды.
    - shift (int): Смещение в битах.
    - bit_length (int): Длина извлекаемого поля.
  - Возвращает: целое число, знаковое (если применимо).

3. `interpret`

  - Описание: считывает двоичные инструкции, выполняет их, обновляет память и генерирует лог.
  - Аргументы:
    - binary_file (str): Имя входного файла с бинарными данными.
    - result_file (str): Имя файла для записи результата.
    - memory_range (tuple): Диапазон памяти для сохранения в результат.
  - Возвращает: Нет. Результаты сохраняются в файле.

4. `main (встроенная)`

  - Описание: Проверяет аргументы командной строки и вызывает функцию interpret.
  - Аргументы: Принимает аргументы командной строки.
  - Возвращает: Нет.

#### Реализация операций

Запуск ассемблера и интерпретатора через командную строку

![image](https://github.com/user-attachments/assets/c62dd446-8d8d-49e6-a20c-d6d1c9e63c38)


##### Загрузка константы 

| A                | B             | C           |
| ---------------- | ------------- | ------------|
| Биты 0-4         | Биты 5-18     | Биты 19-47  |
| Код команды (19) | Адрес         | Константа   |

**Размер команды:** 7 байт

**Операнд:** Поле C

**Результат:** значение в памяти по адресу, которым является поле B.


**Тест** (A=19, B=820, C=213):
```
0x93, 0x66, 0xA8, 0x06, 0x00, 0x00, 0x00
```

**Результат отработки программы:**

Прописывание команды в файле ```program.txt```:
![image](https://github.com/user-attachments/assets/d5076234-ae10-4bb5-87d9-8e3d2c6cd7dd)

Файл ```log.yaml``` после отработки программы:
![image](https://github.com/user-attachments/assets/4e55dbef-b3d5-4287-bf5c-585f5becd1a3)


Файл ```result.yaml``` после отработки программы:
![image](https://github.com/user-attachments/assets/1fe91b8a-407c-4105-8fc9-24fba08f1b81)



##### Чтение значения из памяти 

| A                | B             | C           |
| ---------------- | ------------- | ------------|
| Биты 0-4         | Биты 5-18     | Биты 19-32  |
| Код команды (22) | Адрес         | Адрес       |

**Размер команды:** 7 байт.

**Операнд:** значение в памяти по адресу, которым является значение в памяти по адресу, которым является поле B.

**Результат:** значение в памяти по адресу, которым является поле C.


**Тест** (A=22, B=576, C=52):
```
0x16, 0x48, 0xA0, 0x01, 0x00, 0x00, 0x00
```

**Результат отработки программы:**

Прописывание команды в файле ```program.txt```:
![image](https://github.com/user-attachments/assets/3c66b945-134e-4c08-8f8d-55da2895c1a0)


Файл ```log.yaml``` после отработки программы:
![image](https://github.com/user-attachments/assets/e64f27d2-ab26-4336-b2ac-2b010397e8ec)



Файл ```result.yaml``` после отработки программы:
![image](https://github.com/user-attachments/assets/bf7faa99-2b14-413a-aa0f-ca86f0b3be87)


##### Запись значения в память 

| A                | B             | C           |
| ---------------- | ------------- | ------------|
| Биты 0-4         | Биты 5-18     | Биты 19-32  |
| Код команды (24) | Адрес         | Адрес       |

**Размер команды:** 7 байт.

**Операнд:** значение в памяти по адресу, которым является поле C.

**Результат:**  значение в памяти по адресу, которым является поле B.


**Тест** (A=24, B=742, C=327):
```
0xD8, 0x5C, 0x38, 0x0A, 0x00, 0x00, 0x00
```

**Результат отработки программы:**

Прописывание команды в файле ```program.txt```:
![image](https://github.com/user-attachments/assets/1ec5873d-fe79-4c3f-a394-c4bfeff66be8)



Файл ```log.yaml``` после отработки программы:
![image](https://github.com/user-attachments/assets/5920aab4-4f56-4062-a1dc-eca9ad4f6bcf)





Файл ```result.yaml``` после отработки программы:
![image](https://github.com/user-attachments/assets/cafb8447-b6ec-400c-aa40-e9b916a1d54f)


##### Унарная операция: abs()

| A                | B             | C           | D         |
| ---------------- | ------------- | ------------| ----------| 
| Биты 0-4         | Биты 5-18     | Биты 19-32  | Биты 33-38|
| Код команды (23) | Адрес         | Адрес       | Смещение  |

**Размер команды:** 7 байт.

**Операнд:** : значение в памяти по адресу, которым является сумма адреса (значение в памяти по адресу, которым является поле C) и смещения (поле D).

**Результат:**   значение в памяти по адресу, которым является поле B.

**Тест** (A=23, B=516, C=671, D=31):
```
0x97, 0x40, 0xF8, 0x14, 0x3E, 0x00, 0x00
```

**Результат отработки программы:**

Прописывание команды в файле ```program.txt```:
![image](https://github.com/user-attachments/assets/a63c46d2-8d87-4e51-9c5f-d0a20140f6e1)



Файл ```log.yaml``` после отработки программы:
![image](https://github.com/user-attachments/assets/699b9366-5987-4a1a-bead-12c6b0658c86)




Файл ```result.yaml``` после отработки программы:
![image](https://github.com/user-attachments/assets/4dd39234-8171-4ccd-a957-bcd6d2cd745b)


#### Реализация тестовой программы

Прописывание команд для реализации тестовой программы в файле ```vector_abs.asm```:
![image](https://github.com/user-attachments/assets/c70f8bb2-b25c-4eb0-9682-17cf177b22bc)

Запуск ассемблера и интерпретатора через командную строку:
![image](https://github.com/user-attachments/assets/c156527b-d0af-4103-a9ce-b9d9090af21c)


Файл ```result.yaml``` после заполнения вектора числами:
![image](https://github.com/user-attachments/assets/0b47be60-fd00-490a-a02f-593d9d1714c6)

Файл ```result.yaml``` после отработки операции abs() для каждого элемента:
![image](https://github.com/user-attachments/assets/cc57fe37-1628-43ff-b865-e3c4eccc79ca)

