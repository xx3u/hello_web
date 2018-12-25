import json
import pytest
from io import StringIO
from unittest import mock
from hello import app


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.fixture
def db_data():
    cart = {
        'notebook': 5,
        'TV': 10,
        'smartphone': 25,
        'flash': 155
    }
    return StringIO(json.dumps(cart))


def test_index(client):
    response = client.get('/')
    response = response.data.decode('utf-8')
    assert 'Hello, my dear customer.' in response


def test_post_items_update(client, db_data):
    with mock.patch('hello.open') as mocked:
        mocked.return_value = db_data
        response = client.post(
            '/items',
            data={
                'notebook_name': 'notebook',
                'notebook_quantity': 5,
                'TV_name': 'TV',
                'TV_quantity': 10
            }
        )
        response = response.data.decode('utf-8')
        assert '<input type="text" value="notebook" name="notebook_name">' in response
        assert '<input type="text" value="5" name="notebook_quantity">' \
            in response
        assert '<input type="text" value="TV" name="TV_name">' in response
        assert '<input type="text" value="10" name="TV_quantity">' \
            in response


def test_post_items_add(client, db_data):
    with mock.patch('hello.open') as mocked:
        mocked.return_value = db_data
        response = client.post(
            '/items',
            data={'_name': 'smartwatch', '_quantity': 55}
        )
        response = response.data.decode('utf-8')
        print(response)
        assert '<input type="text" value="smartwatch" name="smartwatch_name">' in response
        assert '<input type="text" value="55" name="smartwatch_quantity">' \
            in response
        

def test_post_items_remove(client, db_data):
    with mock.patch('hello.open') as mocked:
        mocked.return_value = db_data
        response = client.post(
            '/items', data={
                'flash_name': 'flash',
                'flash_quantity': 155,
                'flash_delete': 'on'
            }
        )
        response = response.data.decode('utf-8')
        assert 'flash' not in response
