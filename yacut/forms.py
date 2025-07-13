from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class LinkForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(DataRequired(message='Обязательное поле'),
                    Length(1, 2048))
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=(Length(1, 16), Optional())
    )
    submit = SubmitField('Добавить')


class FileForm(FlaskForm):
    files = MultipleFileField(
        validators=[
            FileAllowed(
                ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
                message=(
                    'Выберите файлы с расширением '
                    '.jpg, .jpeg, .png, .gif или .bmp'
                )
            )
        ]
    )
    submit = SubmitField('Добавить')
