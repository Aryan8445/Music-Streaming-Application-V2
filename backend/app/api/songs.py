from flask import Blueprint, jsonify
from flask_restful import Resource, reqparse, marshal_with, fields, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Song, User, db, Admin
from datetime import datetime


api_bp = Blueprint('Song_api', __name__)
api = Api(api_bp)

song_parser = reqparse.RequestParser()
song_parser.add_argument('title', type=str, required=True, help='Title is required')
song_parser.add_argument('release_date', type=str, required=True, help='Release date is required')
song_parser.add_argument('genre', type=str, required=True, help='Genre is required')
song_parser.add_argument('file_path', type=str, required=True, help='File path is required')
song_parser.add_argument('lyrics', type=str)

song_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'release_date': fields.DateTime(dt_format='iso8601'),
    'genre': fields.String,
    'file_path': fields.String,
    'lyrics': fields.String,
    'artist': fields.String(attribute=lambda x: f"{x.artist.firstname} {x.artist.lastname}")
}


class SongListResource(Resource):
    @jwt_required()
    @marshal_with(song_fields)
    def get(self):
        try:
            songs = Song.query.all()
            return songs
        except Exception as e:
            return {'message': 'An error occurred while fetching songs'}, 500

    @jwt_required()
    @marshal_with(song_fields)
    def post(self):
        try:
            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()

            args = song_parser.parse_args()
            title = args['title']
            release_date = datetime.strptime(args['release_date'], '%Y-%m-%d')
            genre = args['genre']
            file_path = args['file_path']
            lyrics = args['lyrics']

            new_song = Song(title=title, release_date=release_date, genre=genre, file_path=file_path, lyrics=lyrics, artist=current_user)
            db.session.add(new_song)
            db.session.commit()

            return new_song, 201
        except Exception as e:
            return {'message': 'An error occurred while adding a new song'}, 500

class SongResource(Resource):
    @jwt_required()
    @marshal_with(song_fields)
    def put(self, song_id):
        try:
            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()

            song = Song.query.get(song_id)
            if not song:
                return {'message': 'Song not found'}, 404

            # Check if the current user is the artist of the song
            if song.artist != current_user:
                return {'message': 'Unauthorized'}, 401

            args = song_parser.parse_args()
            song.title = args.get('title', song.title)
            song.release_date = datetime.strptime(args.get('release_date', str(song.release_date)), '%Y-%m-%d')
            song.genre = args.get('genre', song.genre)
            song.file_path = args.get('file_path', song.file_path)
            song.lyrics = args.get('lyrics', song.lyrics)

            db.session.commit()

            return song, 200
        except Exception as e:
            return {'message': 'An error occurred while updating the song'}, 500

    @jwt_required()
    def delete(self, song_id):
        try:
            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()

            song = Song.query.get(song_id)
            if not song:
                return {'message': 'Song not found'}, 404

            admin = Admin.query.filter_by(email=current_user_email).first()
            if admin:
                db.session.delete(song)
                db.session.commit()
                return {'message': 'Song deleted successfully'}, 200

            # Check if the current user is the artist of the song
            if song.artist != current_user:
                return {'message': 'Unauthorized'}, 401

            db.session.delete(song)
            db.session.commit()

            return {'message': 'Song deleted successfully'}, 200
        except Exception as e:
            return {'message': 'An error occurred while deleting the song'}, 500

api.add_resource(SongListResource, '/songs')
api.add_resource(SongResource, '/songs/<int:song_id>')
