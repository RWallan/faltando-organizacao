from http import HTTPStatus


def test_create_user_must_return_a_user(client):
    response = client.post(
        '/users',
        json={
            'name': 'Teste',
            'email': 'test@test.com',
            'password': 'test1234',
            'course': 'Teste',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'Teste',
        'email': 'test@test.com',
        'course': 'Teste',
    }


def test_create_existant_user_must_return_error(client, user):
    response = client.post(
        '/users',
        json={
            'name': 'Teste',
            'email': 'test@test.com',
            'password': 'test1234',
            'course': 'Teste',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email já existe.'
