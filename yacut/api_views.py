from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/opinions/<string:short_id>/', methods=['GET'])
def get_opinion(short_id):
    if url_map := URLMap.query.filter_by(short=short_id).first() is None:
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)
    return jsonify({'url': url_map['original']}), 200


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if 'url' not in data or 'custom_id' not in data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage('Такая короткая ссылка ужеесть в базе данных')
    url_map = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201
