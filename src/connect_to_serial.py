import serial

class SerialDevice:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def open(self):
        '''Открывает последовательный порт.'''
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Порт {self.port} открыт.")
            return self.serial
        except serial.SerialException as e:
            print(f"Ошибка открытия порта: {e}")

    def close(self):
        '''Закрывает последовательный порт.'''
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Порт закрыт.")

    def send(self, data):
        '''Отправляет данные на устройство.'''
        if self.serial and self.serial.is_open:
            if isinstance(data, str):
                data = data.encode()
            self.serial.write(data)
            print(f"Отправлено: {data}")
        else:
            print("Порт не открыт.")

    def receive(self):
        '''Получает данные от устройства.'''
        if self.serial and self.serial.is_open:
            data = self.serial.readline()
            print(f"Получено: {data}")
            return data
        else:
            print("Порт не открыт.")
            return None

    def __del__(self):
        '''При удалении объекта класса, закрывает порт.'''
        self.close()
