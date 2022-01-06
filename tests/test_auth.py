import pytest

from chai_py import auth, defaults


@pytest.fixture
def guest_credentials():
    return auth.ChaiAuth(defaults.GUEST_UID, defaults.GUEST_KEY)


def test_guest_credentials(guest_credentials):
    assert guest_credentials.is_guest
    assert guest_credentials.uid == defaults.GUEST_UID
    assert guest_credentials.key == defaults.GUEST_KEY


@pytest.fixture
def dummy_user_credentials():
    return auth.ChaiAuth('test_uid', 'test_key')


def test_non_guest_credentials(dummy_user_credentials):
    assert not dummy_user_credentials.is_guest
    assert dummy_user_credentials.uid == 'test_uid'
    assert dummy_user_credentials.key == 'test_key'
