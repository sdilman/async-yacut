import os

from flask import flash, redirect, render_template, url_for
from werkzeug.utils import secure_filename

from . import app, db
from .forms import FileForm, LinkForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LinkForm()
    
    if form.validate_on_submit():
        custom_id = form.custom_id.data or get_unique_short_id()
        
        if URLMap.query.filter_by(short=custom_id).first():
            flash('Этот короткий идентификатор уже занят!', 'error')
            return render_template('index.html', form=form)
        
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        
        flash('Ссылка успешно сокращена!', 'success')
        short_url = url_for('redirect_to_original', short_id=custom_id, _external=True)
        return render_template('index.html', form=form, short_url=short_url)
    
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)


@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    form = FileForm()
    
    if form.validate_on_submit():
        if not form.files.data or all(file.filename == '' for file in form.files.data):
            flash('Выберите хотя бы один файл', 'danger')
            return redirect(url_for('upload_files'))

        saved_files = []
        for file in form.files.data:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # TODO: исправить на яндекс диск
                if os.path.exists(file_path):
                    flash(f'Файл {filename} уже существует', 'warning')
                    continue
                file.save(file_path)
                saved_files.append(filename)
        
        if saved_files:
            flash(f'Успешно загружено {len(saved_files)} файлов', 'success')
        return redirect(url_for('upload_files'))
    
    return render_template('upload.html', form=form)