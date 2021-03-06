import pytest
import webtest
import os
from learning_journal.models import Entry
from learning_journal import main
import passlib


AUTH_DATA = {'username': 'admin', 'password': 'secret'}


@pytest.fixture()
def app():
    settings = {'sqlalchemy.url': 'postgres://roboiris:secret@localhost:5432/test_journal'}
    app = main({}, **settings)
    return webtest.TestApp(app)


@pytest.fixture()
def authenticated_app(app, auth_env):
    app.post('/login', AUTH_DATA)
    return app


@pytest.fixture()
def auth_env():
    from learning_journal.security import pwd_context
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt('secret')
    os.environ['AUTH_USERNAME'] = 'admin'


@pytest.fixture()
def csrf_input():
    response.html.find('input', id='csrf_token')
    input.get('value')


# this is a functional test
def test_no_access_to_view(app):
    response = app.get('/add', status=403)
    assert response.status_code == 403


def test_access_to_view(authenticated_app):
    response = authenticated_app.get('/login', status=200)
    assert response.status_code == 200


def test_password_exists(app):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_stored_password_encrypted(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) != 'secret'


def test_username_exists(app):
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_check_pw_success(auth_env):
    from learning_journal.security import check_password
    password = 'secret'
    assert check_password(password)

def test_check_pw_success(auth_env):
    from learning_journal.security import check_password
    password = 'not secret'
    assert not check_password(password)


# another functional test
def test_get_login_view(app):
    response = app.get('/login')
    assert response.status_code == 200


def test_post_login_success(app, auth_env):
    response = app.get('/login')
    # import pdb; pdb.set_trace()
    response = app.post('/login', params=AUTH_DATA)
    response.html.find('input', id='csrf_token')
    assert response.status_code == 302


def test_post_login_success_redirects_home(app, auth_env):
    response = app.post('/login', AUTH_DATA)
    headers = response.headers
    domain = "http://localhost"
    actual_path = headers.get('Location', '')[len(domain):]
    assert actual_path == '/'


def test_post_login_success_auth_tkt_present(app, auth_env):
    response = app.post('/login', AUTH_DATA)
    headers = response.headers
    cookies_set = headers.getall('Set-Cookie')
    assert cookies_set
    for cookie in cookies_set:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False


def test_post_login_fail(app, auth_env):
    data = {'username': 'admin', 'password': 'blahh'}
    response = app.post('/login', data)
    assert response.status_code == 200
