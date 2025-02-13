import time

class SerialDevice:
    def __init__(self, port):
        self.port = port
        self.is_open = False
        self.buffer = []

    def open(self):
        if not self.is_open:
            self.is_open = True
            print(f"Serial порт {self.port} открыт.")

    def close(self):
        if self.is_open:
            self.is_open = False
            print(f"Serial порт {self.port} закрыт.")

    def read(self, size=1):
        if not self.is_open:
            raise Exception("Serial порт не открыт.")
        time.sleep(0.1)  # Имитация задержки ответа
        if len(self.buffer) == 0:
            return b''  # Нет данных для чтения
        data = self.buffer[:size]
        self.buffer = self.buffer[size:]
        return bytes(data)

    def write(self, data):
        if not self.is_open:
            raise Exception("Serial порт не открыт.")
        print(f"Запись в serial {self.port}: {data}")
        self.buffer.extend(data)  # Имитировать запись данных на устройство

    def simulate_incoming_data(self, data):
        """Имитировать поступающие данные с устройства."""
        if data == b'GET_V':
            data = b"V_12V"
        elif data == b'GET_A':
            data = b"A_1A"
        elif data == b'GET_S':
            data = b"S_DSA123"
        self.buffer.extend(data)
        print(f"Имитация поступающих данных: {data}")


class SerialClient:
    def __init__(self, device):
        self.device = device

    def connect(self):
        self.device.open()

    def send_data(self, data):
        self.device.write(data)

    def receive_data(self, size=1):
        return self.device.read(size)

    def simulate_incoming_data(self, data):
        self.device.simulate_incoming_data(data)

    def __del__(self):
        self.device.close()
