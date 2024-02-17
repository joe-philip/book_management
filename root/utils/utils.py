from datetime import datetime
from typing import Any

from django.utils.text import slugify
from pytz import timezone


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


def slug_generate(key: str = 'slug') -> str:
    slugify(f'{key}-{datetime.now(tz=timezone("Asia/Calcutta")).timestamp()}')
