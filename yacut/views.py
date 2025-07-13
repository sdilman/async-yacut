from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import FileForm, LinkForm
from .models import URLMap
from .utils import get_unique_short_id
from .ya_disk import async_upload_files


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
async def upload_files():
    form = FileForm()
    
    if form.validate_on_submit():
        file_names = [file.filename for file in form.files.data]
        if not form.files.data or all(file_name == '' for file_name in file_names):
            flash('Выберите хотя бы один файл', 'danger')
            return redirect(url_for('upload_files'))
        urls = await async_upload_files(form.files.data)
        # сделать короткие ссылки, сохранить их, и в html сделать переход на redirect_to_original
        #return redirect(url_for('upload_files', urls=urls))
        return render_template(
            'upload.html',
            form=form,
            file_info=zip(file_names, urls)
        )
    
    return render_template('upload.html', form=form)
