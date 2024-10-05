"""
coding:utf-8
file: photo.py
@time: 2024/10/5 0:09
@desc:
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from blogin.models import Photo
from blogin.api.decorators import get_params, check_permission
from blogin.responses import R


api_photo_bp = Blueprint('api_photo_bp', __name__, url_prefix='/api/photo')


@api_photo_bp.route('/list', methods=['GET'])
@get_params(
    params=['page', 'limit', 'name', 'level'],
    types=[int, int, str, str],
    remove_none=True
)
@jwt_required
@check_permission
def photo_list(page, limit=12, name='', level=None):
    query = (Photo.id > 0,)

    if name:
        query += (Photo.title.contains(name),)

    if level is not None:
        query += (Photo.level == level,)

    photos = Photo.query.filter(
        *query
    ).order_by(
        Photo.create_time.desc()
    ).paginate(
        per_page=limit,
        page=page,
    )

    data = []
    for photo in photos.items:
        item = photo.to_dict()
        item['tags'] = [tag.name for tag in photo.tags]
        item['comments'] = len(photo.comments)
        item['likes'] = len(photo.likes)
        item['url'] = photo.url(small=True)
        data.append(item)

    return R.success(
        total=photos.total,
        data=data
    )


@api_photo_bp.route('/origin-image', methods=['GET'])
@jwt_required
@check_permission
def origin_image():
    photo_id = request.args.get('id')
    photo = Photo.query.get(photo_id)
    if not photo:
        return R.not_found()

    return R.success(
        url=photo.url(small=False)
    )
