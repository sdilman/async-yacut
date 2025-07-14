from flask import jsonify, request, url_for
import re

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .link_processor import get_unique_short_id


SHORT_LINK_ID_PATTERN = r'^[a-zA-Z0-9]{1,16}$'
ORIGINAL_LINK_ID_PATTERN = r'^https?://.+'

@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_link(short_id):
    if (url_map := URLMap.query.filter_by(short=short_id).first()) is None:
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)
    return jsonify({'url': url_map.original}), 200


@app.route('/api/id/', methods=('POST',))
def add_link():
    if int(request.headers.get('Content-Length', 0)) == 0:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    data = request.get_json()

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not re.fullmatch(ORIGINAL_LINK_ID_PATTERN, data['url']):
        raise InvalidAPIUsage('Указан недопустимый "url"')

    if (
        'custom_id' in data
        and data['custom_id'] != ''
        and not re.fullmatch(SHORT_LINK_ID_PATTERN, data['custom_id'])
    ):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if (
        'custom_id' in data
        and URLMap.query.filter_by(short=data['custom_id']).first() is not None
    ):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    if 'custom_id' in data and data['custom_id'] != '':
        custom_id = data['custom_id']
    else:
        custom_id = get_unique_short_id()

    url_map = URLMap.create(data['url'], data.get('custom_id', custom_id))
    return jsonify(
        dict(
            url=url_map.original,
            short_link=url_for(
                'redirect_to_original',
                short_id=url_map.short,
                _external=True
            )
        )
    ), 201
