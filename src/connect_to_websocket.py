import websocket
import threading
import time

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.thread = None
        self.running = False

    def on_message(self, ws, message):
        print(f'Полученное сообщение: {message}')

    def on_error(self, ws, error):
        print(f'Ошибка: {error}')

    def on_close(self, ws):
        print('Соединение закрыто')

    def on_open(self, ws):
        print('Соединение открыто')
        self.running = True

    def run(self):
        self.ws = websocket.WebSocketApp(self.url,
                                          on_message=self.on_message,
                                          on_error=self.on_error,
                                          on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()

    def stop(self):
        self.running = False
        self.ws.close()
        self.thread.join()

    def send(self, message):
        if self.ws and self.ws.sock and self.ws.sock.connected:
            self.ws.send(message)
            print(f'Отправленное сообщение: {message}')
        else:
            print('Веб-сокет не подключен')
    
    def __del__(self):
        '''При удалении объекта класса, закрывает сокет.'''
        self.stop()

# Пример использования
if __name__ == '__main__':
    url = 'ws://echo.websocket.org'  # Замените на ваш URL веб-сокета
    client = WebSocketClient(url)
    client.run()

    try:
        while client.running:
            time.sleep(1)  # Задержка для ожидания сообщений
            client.send('Hello again!')  # Отправка сообщения
    except KeyboardInterrupt:
        client.stop()