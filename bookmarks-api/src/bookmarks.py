from flask import Blueprint, request
from constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Bookmarks, db

bookmarks = Blueprint(
    'bookmarks',
     __name__, 
     url_prefix='/api/v1/bookmarks', 
    )



@bookmarks.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()

    if request.method == 'POST':

        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            }), HTTP_400_BAD_REQUEST

        if Bookmarks.query.filter_by(url=url).first():
            return jsonify({
                'error': 'URL already exists'
            }), HTTP_409_CONFLICT

        Bookmarks = Bookmarks(url=url, body=body, user_id=current_user)
        db.session.add(Bookmarks)
        db.session.commit()

        return jsonify({
            'id': Bookmarks.id,
            'url': Bookmarks.url,
            'short_url': Bookmarks.short_url,
            'visit': Bookmarks.visits,
            'body': Bookmarks.body,
            'created_at': Bookmarks.created_at,
            'updated_at': Bookmarks.updated_at,
        }), HTTP_201_CREATED

    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        bookmarks = Bookmarks.query.filter_by(
            user_id=current_user).paginate(page=page, per_page=per_page)

        data = []

        for Bookmarks in bookmarks.items:
            data.append({
                'id': Bookmarks.id,
                'url': Bookmarks.url,
                'short_url': Bookmarks.short_url,
                'visit': Bookmarks.visits,
                'body': Bookmarks.body,
                'created_at': Bookmarks.created_at,
                'updated_at': Bookmarks.updated_at,
            })

        meta = {
            "page": bookmarks.page,
            'pages': bookmarks.pages,
            'total_count': bookmarks.total,
            'prev_page': bookmarks.prev_num,
            'next_page': bookmarks.next_num,
            'has_next': bookmarks.has_next,
            'has_prev': bookmarks.has_prev,

        }

        return jsonify({'data': data, "meta": meta}), HTTP_200_OK
    
@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()

    Bookmarks = Bookmarks.query.filter_by(user_id=current_user, id=id).first()

    if not Bookmarks:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    return jsonify({
        'id': Bookmarks.id,
        'url': Bookmarks.url,
        'short_url': Bookmarks.short_url,
        'visit': Bookmarks.visits,
        'body': Bookmarks.body,
        'created_at': Bookmarks.created_at,
        'updated_at': Bookmarks.updated_at,
    }), HTTP_200_OK


@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()

    Bookmarks = Bookmarks.query.filter_by(user_id=current_user, id=id).first()

    if not Bookmarks:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(Bookmarks)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT


@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()
def editbookmark(id):
    current_user = get_jwt_identity()

    Bookmarks = Bookmarks.query.filter_by(user_id=current_user, id=id).first()

    if not Bookmarks:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')

    if not validators.url(url):
        return jsonify({
            'error': 'Enter a valid url'
        }), HTTP_400_BAD_REQUEST

    Bookmarks.url = url
    Bookmarks.body = body

    db.session.commit()

    return jsonify({
        'id': Bookmarks.id,
        'url': Bookmarks.url,
        'short_url': Bookmarks.short_url,
        'visit': Bookmarks.visits,
        'body': Bookmarks.body,
        'created_at': Bookmarks.created_at,
        'updated_at': Bookmarks.updated_at,
    }), HTTP_200_OK


@bookmarks.get("/stats")
@jwt_required()
# @swag_from("./docs/bookmarks/stats.yaml")
def get_stats():
    current_user = get_jwt_identity()

    data = []

    items = Bookmarks.query.filter_by(user_id=current_user).all()

    for item in items:
        new_link = {
            'visits': item.visits,
            'url': item.url,
            'id': item.id,
            'short_url': item.short_url,
        }

        data.append(new_link)

    return jsonify({'data': data}), HTTP_200_OK