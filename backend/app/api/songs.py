from flask import Blueprint, jsonify, request, current_app
from flask_restful import Resource, reqparse, marshal_with, fields, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Song, User, db, Admin,Rating
from datetime import datetime
from werkzeug.utils import secure_filename
import os


api_bp = Blueprint('Song_api', __name__)
api = Api(api_bp)

song_parser = reqparse.RequestParser()
song_parser.add_argument('title', type=str, required=True, help='Title is required')
song_parser.add_argument('release_date', type=str, required=True, help='Release date is required')
song_parser.add_argument('genre', type=str, required=True, help='Genre is required')
song_parser.add_argument('lyrics', type=str)


song_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'release_date': fields.DateTime(dt_format='iso8601'),
    'genre': fields.String,
    'file_path': fields.String,
    'lyrics': fields.String,
    'artist': fields.String(attribute=lambda x: f"{x.artist.firstname} {x.artist.lastname}"),
}


class SongListResource(Resource):
    @marshal_with(song_fields)
    def get(self):
        try:
            songs = Song.query.all()
            return songs
        except Exception as e:
            return {'message': 'An error occurred while fetching songs'}, 500

class SongUploadResource(Resource):
    @marshal_with(song_fields)
    @jwt_required()
    def post(self):
        try:
            title = request.form['title']
            release_date = datetime.strptime(request.form['release_date'], '%Y-%m-%d')
            genre = request.form['genre']
            lyrics = request.form['lyrics']

            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()

            if 'song_file' not in request.files:
                return {'message': 'No file part'}, 400
            
            song_file = request.files['song_file']

            if song_file.filename == '':
                return {'message': 'No selected file'}, 400

            if song_file:
                # Generate a unique filename
                filename = secure_filename(song_file.filename)
                # Save the file to the designated folder
                songs_dir = os.path.join(current_app.root_path, 'static', 'songs')
                os.makedirs(songs_dir, exist_ok=True)
                file_path = os.path.join(songs_dir, filename)
                song_file.save(file_path)

                # Construct the URL to access the file from the frontend
                base_url = request.url_root.rstrip('/')
                file_url = f"{base_url}/static/songs/{filename}"

                # Create a new song record in the database
                new_song = Song(
                    title=title,
                    release_date=release_date,
                    genre=genre,
                    file_path=file_url,  # Update file_path with the URL
                    lyrics=lyrics,
                    artist_id=current_user.id
                )
                current_user.user_type = 'creator'
                db.session.add(new_song)
                db.session.commit()

                return new_song, 201
            else:
                return {'message': 'Invalid or missing song file'}, 400
        except Exception as e:
            return {'message': 'An error occurred while uploading the song'}, 500





class SongResource(Resource):
    @marshal_with(song_fields)
    def get(self, song_id):
        try:
            song = Song.query.get(song_id)
            if not song:
                return {'message': 'Song not found'}, 404

            return song, 200
        except Exception as e:
            return {'message': 'An error occurred while fetching the song'}, 500

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
                # Delete associated ratings
                Rating.query.filter_by(song_id=song_id).delete()
                # Delete the song
                db.session.delete(song)
                db.session.commit()
                return {'message': 'Song and associated ratings deleted successfully'}, 200

            # Check if the current user is the artist of the song
            if song.artist != current_user:
                return {'message': 'Unauthorized'}, 401

            # Delete associated ratings
            Rating.query.filter_by(song_id=song_id).delete()
            # Delete the song
            db.session.delete(song)
            db.session.commit()

            return {'message': 'Song and associated ratings deleted successfully'}, 200
        except Exception as e:
            return {'message': 'An error occurred while deleting the song'}, 500

class CreatorSongsResource(Resource):
    @marshal_with(song_fields)
    def get(self, creator_id):
        try:
            songs = Song.query.filter_by(artist_id=creator_id).all()
            if not songs:
                return {'message': 'No songs found for this creator'}, 404

            return songs, 200
        except Exception as e:
            return {'message': 'An error occurred while fetching songs for this creator'}, 500
api.add_resource(CreatorSongsResource, '/songs/creator/<int:creator_id>')
api.add_resource(SongListResource, '/songs')
api.add_resource(SongUploadResource, '/songs/upload')
api.add_resource(SongResource, '/songs/<int:song_id>')
