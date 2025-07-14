from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


MAX_ORIGINAL_LINK_LENGTH = 2048
MAX_SHORT_LINK_LENGTH = 16


class LinkForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(
            DataRequired(message='Обязательное поле'),
            Length(max=MAX_ORIGINAL_LINK_LENGTH)
        )
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=(
            Optional(),
            Length(max=MAX_SHORT_LINK_LENGTH),
            Regexp(
                r'^[a-zA-Z0-9]+$',
                message='Допустимы только латинские буквы и цифры'
            )
        )
    )
    submit = SubmitField('Добавить')


class FileForm(FlaskForm):
    files = MultipleFileField(
        validators=[
            FileAllowed(
                ('jpg', 'jpeg', 'png', 'gif', 'bmp'),
                message=(
                    'Выберите файлы с расширением '
                    '.jpg, .jpeg, .png, .gif или .bmp'
                )
            )
        ]
    )
    submit = SubmitField('Добавить')
