from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from sqlalchemy.exc import SQLAlchemyError
from app.models import Album, User, db, Admin, Song

api_bp = Blueprint('Album_api', __name__)
api = Api(api_bp)

album_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'artist_id': fields.Integer
    # Add more fields as needed
}

# Custom decorator to check if user is authorized as creator or admin
def creator_or_admin_required(fn):
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if user.user_type == 'creator' or Admin.query.filter_by(name=current_user_email).first():
            return fn(*args, **kwargs)
        else:
            return {'message': 'Unauthorized'}, 401
    return wrapper

class AlbumListResource(Resource):
    @jwt_required()
    @marshal_with(album_fields)
    def get(self):
        try:
            albums = Album.query.all()
            return albums
        except SQLAlchemyError:
            return {'message': 'An error occurred while fetching albums'}, 500

    @jwt_required()
    @marshal_with(album_fields)
    @creator_or_admin_required
    def post(self):
        try:
            data = request.get_json()
            title = data.get('title')
            song_ids = data.get('song_ids', [])
            # Add more fields as needed

            new_album = Album(title=title)
            # Set other fields as needed

            for song_id in song_ids:
                song = Song.query.get(song_id)
                if song:
                    new_album.songs.append(song)

            db.session.add(new_album)
            db.session.commit()

            return new_album, 201
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'An error occurred while creating an album'}, 500

class AlbumResource(Resource):
    @jwt_required()
    @marshal_with(album_fields)
    @creator_or_admin_required
    def put(self, album_id):
        try:
            data = request.get_json()
            new_title = data.get('title')
            # Update other fields as needed

            album = Album.query.get(album_id)
            if not album:
                return {'message': 'Album not found'}, 404

            album.title = new_title
            # Update other fields as needed

            db.session.commit()

            return album, 200
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'An error occurred while updating the album'}, 500

    @jwt_required()
    @creator_or_admin_required
    def delete(self, album_id):
        try:
            album = Album.query.get(album_id)
            if not album:
                return {'message': 'Album not found'}, 404

            db.session.delete(album)
            db.session.commit()

            return {'message': 'Album deleted successfully'}, 200
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({'message': 'An error occurred while deleting the album'}), 500

class AlbumAddSongResource(Resource):
    @jwt_required()
    @marshal_with(album_fields)
    @creator_or_admin_required
    def post(self, album_id):
        try:
            album = Album.query.get(album_id)
            if not album:
                return {'message': 'Album not found'}, 404

            data = request.get_json()
            song_id = data.get('song_id')
            song = Song.query.get(song_id)
            if not song:
                return {'message': 'Song not found'}, 404

            album.songs.append(song)
            db.session.commit()

            return album, 200
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'An error occurred while adding a song to the album'}, 500

class AlbumDeleteSongResource(Resource):
    @jwt_required()
    @marshal_with(album_fields)
    @creator_or_admin_required
    def delete(self, album_id, song_id):
        try:
            album = Album.query.get(album_id)
            if not album:
                return {'message': 'Album not found'}, 404

            song = Song.query.get(song_id)
            if not song:
                return {'message': 'Song not found'}, 404

            if song not in album.songs:
                return {'message': 'Song not in album'}, 404

            album.songs.remove(song)
            db.session.commit()

            return album, 200
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'An error occurred while deleting the song from the album'}, 500

api.add_resource(AlbumListResource, '/albums')
api.add_resource(AlbumResource, '/albums/<int:album_id>')
api.add_resource(AlbumAddSongResource, '/albums/<int:album_id>/add-song')
api.add_resource(AlbumDeleteSongResource, '/albums/<int:album_id>/delete-song/<int:song_id>')
