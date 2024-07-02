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


def test_get_user_by_id_must_return_a_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'name': 'Teste',
        'email': 'test@test.com',
        'course': 'Teste',
    }


def test_get_not_existant_user_must_return_error(client, user):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Usuário não encontrado.'


def test_update_user_must_return_user(client, user):
    response = client.put(f'/users/{user.id}', json={'name': 'TesteStr'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'TesteStr',
        'email': 'test@test.com',
        'course': 'Teste',
    }


def test_update_not_existant_user_must_return_error(client, user):
    response = client.put('/users/2', json={'name': 'TesteStr'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Usuário não encontrado.'
