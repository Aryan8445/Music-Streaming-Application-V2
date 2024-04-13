from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app.models import Album, User, Song, db, Admin
from functools import wraps

api_bp = Blueprint('Album_api', __name__)
api = Api(api_bp)

album_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'artist_id': fields.Integer,
    'artist_email': fields.String(attribute=lambda x: x.artist.email),
    'artist': fields.String(attribute=lambda x: f"{x.artist.firstname} {x.artist.lastname}"),
    'songs': fields.List(fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'release_date': fields.DateTime(dt_format='iso8601'),
        'genre': fields.String,
        'file_path': fields.String,
        'lyrics': fields.String,
        'artist_id': fields.Integer,
        'artist': fields.String(attribute=lambda x: f"{x.artist.firstname} {x.artist.lastname}")
    }))
}

def creator_or_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=current_user_email).first()
        admin = Admin.query.filter_by(email=current_user_email).first()

        if current_user and current_user.user_type == "creator":
            return fn(*args, **kwargs)
        elif admin:
            return fn(*args, **kwargs)
        else:
            return {'message': 'Unauthorized'}, 401

    return wrapper

class AlbumListResource(Resource):
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

            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(
                email=current_user_email).first()
            if not current_user:
                return {'message': 'User not found'}, 404

            new_album = Album(title=title, artist_id=current_user.id)

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

    @marshal_with(album_fields)
    def get(self, album_id):
        try:
            album = Album.query.get(album_id)
            if not album:
                return {'message': 'Album not found'}, 404
            return album, 200
        except SQLAlchemyError:
            return {'message': 'An error occurred while fetching the album'}, 500

    @jwt_required()
    @marshal_with(album_fields)
    @creator_or_admin_required
    def put(self, album_id):
        try:
            data = request.get_json()
            new_title = data.get('title')

            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(
                email=current_user_email).first()
            if not current_user:
                return {'message': 'User not found'}, 404

            album = Album.query.filter_by(
                id=album_id, artist_id=current_user.id).first()
            if not album:
                return {'message': 'Album not found'}, 404

            album.title = new_title
            db.session.commit()

            return album, 200
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'An error occurred while updating the album'}, 500

    @jwt_required()
    @creator_or_admin_required
    def delete(self, album_id):
        try:
            current_user_email = get_jwt_identity()
            album = Album.query.get(album_id)
            if not album:
                return {'message': 'Album not found'}, 404
            
            admin = Admin.query.filter_by(email=current_user_email).first()
            if admin:
                db.session.delete(album)
                db.session.commit()
                return {'message': 'Album deleted successfully'}, 200
            
            current_user = User.query.filter_by(
                email=current_user_email).first()
            if not current_user:
                return {'message': 'User not found'}, 404

            


            elif current_user.user_type == "creator" and album.artist_id != current_user.id:
                return {'message': 'Unauthorized'}, 401
            else:
                db.session.delete(album)
                db.session.commit()
                return {'message': 'Album deleted successfully'}, 200
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'An error occurred while deleting the album'}, 500

class AlbumAddSongResource(Resource):
    @jwt_required()
    @marshal_with(album_fields)
    @creator_or_admin_required
    def post(self, album_id):
        try:
            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(
                email=current_user_email).first()
            if not current_user:
                return {'message': 'User not found'}, 404

            album = Album.query.get(album_id)
            if not album:
                return {'message': 'Album not found'}, 404

            # Check if the current user is the creator of the album
            if album.artist_id != current_user.id:
                return {'message': 'Unauthorized'}, 401

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
            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(
                email=current_user_email).first()
            if not current_user:
                return {'message': 'User not found'}, 404

            album = Album.query.get(album_id)
            if not album:
                return {'message': 'Album not found'}, 404

            # Check if the current user is the creator of the album
            if album.artist_id != current_user.id:
                return {'message': 'Unauthorized'}, 401

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
api.add_resource(AlbumDeleteSongResource,'/albums/<int:album_id>/delete-song/<int:song_id>')
