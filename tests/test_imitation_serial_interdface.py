import pytest
from time import sleep
from src.imitation_serial_device import SerialDevice, SerialClient

class Connections:
    @pytest.fixture(scope='module')
    def serial_console_connection(self) -> SerialDevice:
        '''Создание сесии для serial'''
        serial_device = SerialDevice(port="/dev/ttyUSB0")
        client = SerialClient(device=serial_device)
        client.connect()
        return client

class Utils(Connections):
    @pytest.fixture(scope='function')
    def requests_get_v(self, serial_console_connection: SerialClient) -> str:
        '''Получение ответа на запрос GET_V'''
        serial_console_connection.simulate_incoming_data(b'GET_V')
        sleep(1)
        return serial_console_connection.receive_data(5)

    @pytest.fixture(scope='function')
    def requests_get_a(self, serial_console_connection: SerialClient) -> str:
        '''Получение ответа на запрос GET_A'''
        serial_console_connection.simulate_incoming_data(b'GET_A')
        sleep(1)
        return serial_console_connection.receive_data(5)

    @pytest.fixture(scope='function')
    def requests_get_s(self, serial_console_connection: SerialClient) -> str:
        '''Получение ответа на запрос GET_S'''
        serial_console_connection.simulate_incoming_data(b'GET_S')
        sleep(1)
        return serial_console_connection.receive_data(8)

    @pytest.fixture(scope='function')
    def settings(self, request: pytest.FixtureRequest) -> None:
        request.getfixturevalue('requests_get_v')
        request.getfixturevalue('requests_get_a')
        request.getfixturevalue('requests_get_s')

@pytest.mark.usefixtures('settings')
class TestSerialDevite(Utils):
    def test_request_get_v(self, requests_get_v: str) -> None:
        '''Сравненеие ответа на запрос GET_V с ожидаемым'''
        assert requests_get_v == b'V_12V'

    def test_request_get_a(self, requests_get_a: str) -> None:
        '''Сравненеие ответа на запрос GET_A с ожидаемым'''
        assert requests_get_a == b'A_1A'

    def test_request_get_as(self, requests_get_s: str) -> None:
        '''Сравненеие ответа на запрос GET_S с ожидаемым'''
        assert requests_get_s == b'S_DSA123'
