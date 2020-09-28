"""
# coding:utf-8
@Time    : 2020/9/23
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : photo_bp
@Software: PyCharm
"""
from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from blogin.setting import basedir
from blogin.blueprint.backend.forms import AddPhotoForm
from blogin.models import Photo, Tag
from blogin.utils import create_path
from blogin.extension import db
be_photo_bp = Blueprint('be_photo_bp', __name__, url_prefix='/backend')


@be_photo_bp.route('/photo/add/', methods=['GET', 'POST'])
@login_required
def add_photo():
    form = AddPhotoForm()
    if form.validate_on_submit():
        tags = form.tags.data
        title = form.photo_title.data
        img_file = form.img_file.data.filename
        img_file = str(current_user.id) + img_file
        desc = form.photo_desc.data
        folder = str(datetime.now()).split(' ')[0]
        create_path(basedir + '/uploads/gallery/' + folder)
        form.img_file.data.save(basedir + '/uploads/gallery/' + folder + '/' + img_file)
        img_path = '/gallery/' + folder + '/' + img_file
        photo = Photo(title=title, description=desc, save_path=img_path)

        for name in tags.split():
            tag = Tag.query.filter_by(name=name).first()
            if tag is None:
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
            if tag not in photo.tags:
                photo.tags.append(tag)
                db.session.commit()
        flash('相片添加完成~', 'success')
        return redirect(url_for('gallery_bp.index'))
    return render_template('backend/addPhoto.html', form=form)

