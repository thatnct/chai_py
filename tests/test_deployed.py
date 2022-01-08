import mock
import pytest
import requests

from chai_py import deployed as dep
from chai_py import defaults, error


@pytest.fixture(autouse=True)
def set_authentication():
    with mock.patch('chai_py.auth.get_auth') as m:
        m.uid = 'test_uid'
        m.key = 'test_key'
        yield


@mock.patch('requests.get')
def test_get_developer_bots(get):
    raw_response = {'data': [
        {
            'name': 'Eliza', 'bot_uid': '_bot_test123',
            'developer_uid': 'dev_123', 'status': 'inactive'
        },
        {
            'name': 'Daisy', 'bot_uid': '_bot_test999',
            'developer_uid': 'dev_123', 'status': 'active'
        },
    ]}

    get.return_value = mock.Mock(
        status_code=200,
        json=mock.Mock(return_value=raw_response)
    )

    expected = [
        dep.DeployedBot('_bot_test123', 'Eliza', 'dev_123', dep.BotStatus.INACTIVE),
        dep.DeployedBot('_bot_test999', 'Daisy', 'dev_123', dep.BotStatus.ACTIVE)
    ]

    bot = dep.get_bots()
    assert bot == expected


@mock.patch('requests.get')
def test_get_developer_bots_raises_on_error(get):
    get.return_value = mock.Mock(
        status_code=404,
        text='unhandled error'
    )

    with pytest.raises(error.APIError) as ex:
        dep.get_bots()

    assert 'unhandled error' in str(ex)


@mock.patch('requests.post')
def test_activate_bot(post):
    post.return_value = mock.Mock(
        status_code=200,
        json=mock.Mock(return_value={})
    )

    dep.activate_bot('bot_123')

    post.assert_called_with(
        '{}/chatbots/bot_123'.format(defaults.API_HOST),
        json={'status': 'active'},
        auth=mock.ANY
    )


@mock.patch('requests.post')
def test_activate_bot_raises_on_error(post):
    post.return_value = mock.Mock(
        status_code=401,
        text='Permission denied'
    )

    with pytest.raises(error.APIError) as ex:
        dep.activate_bot('bot_123')

    assert '401' in str(ex)
    assert 'Permission denied' in str(ex)


@mock.patch('requests.post')
def test_deactivate_bot(post):
    post.return_value = mock.Mock(
        status_code=200,
        json=mock.Mock(return_value={})
    )

    dep.deactivate_bot('bot_123')

    post.assert_called_with(
        '{}/chatbots/bot_123'.format(defaults.API_HOST),
        json={'status': 'inactive'},
        auth=mock.ANY
    )


@mock.patch('requests.post')
def test_deactivate_bot_raises_on_error(post):
    post.return_value = mock.Mock(
        status_code=401,
        text='Permission denied'
    )

    with pytest.raises(error.APIError) as ex:
        dep.deactivate_bot('bot_123')

    assert '401' in str(ex)
    assert 'Permission denied' in str(ex)
