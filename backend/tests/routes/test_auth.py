from http import HTTPStatus


def test_login(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_pwd},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
