from typing import Any


def fail(error: str) -> dict:
    return {
        'status': False,
        'message': 'fail',
        'error': error
    }


def success(data: Any = None) -> dict:
    response_data = {
        'status': True,
        'message': 'success'
    }
    if data is not None:
        response_data['data'] = data
    return response_data
