from http import HTTPStatus

import pytest

from tests.conftest import TodoFactory


def test_create_todo(client, token):
    data = {
        'title': 'test',
        'description': 'test inclusão de tarefa',
        'state': 'draft',
    }
    response = client.post(
        '/todos', headers={'Authorization': f'Bearer {token}'}, json=data
    )

    data['id'] = 1

    result: dict = response.json()

    result.pop('created_at')
    result.pop('updated_at')

    assert response.status_code == HTTPStatus.OK
    assert result == data


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos', headers={'Authorization': f'Bearer {token}'}
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.parametrize(
    'filter',
    [
        ({'title': 'test todo'}),
        ({'description': 'desc'}),
        ({'state': 'draft'}),
    ],
)
def test_list_todos_filter_should_return_5_todos(
    session, client, user, token, filter
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, **filter, user_id=user.id)
    )
    session.commit()

    query_filter = '&'.join([
        f'{key}={value}' for key, value in filter.items()
    ])

    response = client.get(
        f'/todos/?{query_filter}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.parametrize(
    'filter',
    [
        ({
            'title': 'test todo combined',
            'description': 'combined description',
            'state': 'done',
        }),
        ({
            'title': 'test todo combined',
            'state': 'todo',
        }),
        ({
            'description': 'combined description',
            'state': 'draft',
        }),
    ],
)
def test_list_todos_filter_combined_should_return_5_todos(
    session, client, user, token, filter
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, **filter, user_id=user.id)
    )
    session.bulk_save_objects(TodoFactory.create_batch(3, user_id=user.id))
    session.commit()

    query_filter = '&'.join([
        f'{key}={value}' for key, value in filter.items()
    ])

    response = client.get(
        f'/todos/?{query_filter}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_todo_not_found(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        '/todos/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'test!'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'test!'


def test_patch_todo_not_found(client, token):
    response = client.patch(
        '/todos/10', json={}, headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
