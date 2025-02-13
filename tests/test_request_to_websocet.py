import pytest
from time import sleep
from src.connect_to_websocket import WebSocketClient

URL: str = 'ws://websocket.ru'
GET_REQUESTS: dict = {'cmd1': 'GET_V', 'cmd2': 'GET_A', 'cmd3': 'GET_S'}

class Connections:
    @pytest.fixture(scope='module')
    def websocket_connection(self) -> WebSocketClient:
        '''Создание сесии для websocket'''
        return WebSocketClient(url=URL).run()

class Utils(Connections):
    @pytest.fixture(scope='function')
    def requests_get_v(self, websocket_connection: WebSocketClient) -> dict:
        '''Получение ответа на запрос GET_V'''
        request = websocket_connection.send({'cmd': GET_REQUESTS['cmd1']})
    
    @pytest.fixture(scope='function')
    def requests_get_a(self, websocket_connection: WebSocketClient) -> dict:
        '''Получение ответа на запрос GET_A'''
        return websocket_connection.send({'cmd': GET_REQUESTS['cmd2']})
    
    @pytest.fixture(scope='function')
    def requests_get_s(self, websocket_connection: WebSocketClient) -> dict:
        '''Получение ответа на запрос GET_S'''
        return websocket_connection.send({'cmd': GET_REQUESTS['cmd3']})
    
    @pytest.fixture(scope='function')
    def settings(self, request: pytest.FixtureRequest) -> None:
        request.getfixturevalue('requests_get_v')
        sleep(5)
        request.getfixturevalue('requests_get_a')
        sleep(5)
        request.getfixturevalue('requests_get_s')
        sleep(5)

@pytest.mark.usefixtures('settings') 
class TestWebsocket(Utils):
    def test_request_get_v(self, requests_get_v: str) -> None:
        '''Сравненеие ответа на запрос GET_V с ожидаемым'''
        assert requests_get_v == {'cmd': GET_REQUESTS['cmd1'], 'payload': 'V_12V'}

    def test_request_get_a(self, requests_get_a: str) -> None:
        '''Сравненеие ответа на запрос GET_A с ожидаемым'''
        assert requests_get_a == {'cmd': GET_REQUESTS['cmd2'], 'payload': 'A_12'}
    
    def test_request_get_s(self, requests_get_s: str) -> None:
        '''Сравненеие ответа на запрос GET_S с ожидаемым'''
        assert requests_get_s == {'cmd': GET_REQUESTS['cmd3'], 'payload': 'S_DSA123'}
