import pytest
from time import sleep
from src.connect_to_serial import SerialDevice

class Connections:
    @pytest.fixture(scope='module')
    def serial_console_connection(self) -> SerialDevice:
        '''Создание сесии для serial'''
        return SerialDevice.open(port='/dev/ttyUSB0')

class Utils(Connections):
    @pytest.fixture(scope='function')
    def requests_get_v(self, serial_console_connection: SerialDevice) -> str:
        '''Получение ответа на запрос GET_V'''
        serial_console_connection.send("GET_V")
        sleep(3)
        return serial_console_connection.receive()
    
    @pytest.fixture(scope='function')
    def requests_get_a(self, serial_console_connection: SerialDevice) -> str:
        '''Получение ответа на запрос GET_A'''
        serial_console_connection.send("GET_A")
        sleep(3)
        return serial_console_connection.receive()
    
    @pytest.fixture(scope='function')
    def requests_get_s(self, serial_console_connection: SerialDevice) -> str:
        '''Получение ответа на запрос GET_S'''
        serial_console_connection.send("GET_S")
        sleep(3)
        return serial_console_connection.receive()
    
    @pytest.fixture(scope='function')
    def settings(self, request: pytest.FixtureRequest) -> None:
        request.getfixturevalue('requests_get_v')
        request.getfixturevalue('requests_get_a')
        request.getfixturevalue('requests_get_s')

@pytest.mark.usefixtures('settings') 
class TestSerialDevite(Utils):
    def test_request_get_a(self, requests_get_v: str) -> None:
        '''Сравненеие ответа на запрос GET_V с ожидаемым'''
        assert requests_get_v == 'V_12V'

    def test_request_get_a(self, requests_get_a: str) -> None:
        '''Сравненеие ответа на запрос GET_A с ожидаемым'''
        assert requests_get_a == 'A_12A'
    
    def test_request_get_a(self, requests_get_s: str) -> None:
        '''Сравненеие ответа на запрос GET_S с ожидаемым'''
        assert requests_get_s == 'S_DSA123'