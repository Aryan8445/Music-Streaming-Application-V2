from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app.models import Playlist, User, Song, db

api_bp = Blueprint('Playlist_api', __name__)
api = Api(api_bp)

playlist_fields = {
    'id': fields.Integer,
    'title': fields.String,
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

class PlaylistListResource(Resource):
    @jwt_required()
    @marshal_with(playlist_fields)
    def get(self):
        try:
            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()
            playlists = Playlist.query.filter_by(user_id=current_user.id).all()
            return playlists
        except SQLAlchemyError:
            return jsonify({'message': 'An error occurred while fetching playlists'}), 500

    @jwt_required()
    @marshal_with(playlist_fields)
    def post(self):
        try:
            data = request.get_json()
            title = data.get('title')
            song_ids = data.get('song_ids', [])

            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()

            new_playlist = Playlist(title=title, user_id=current_user.id)

            for song_id in song_ids:
                song = Song.query.get(song_id)
                if song:
                    new_playlist.songs.append(song)

            db.session.add(new_playlist)
            db.session.commit()

            return new_playlist, 201
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({'message': 'An error occurred while creating a playlist'}), 500

class PlaylistResource(Resource):
    @jwt_required()
    @marshal_with(playlist_fields)
    def put(self, playlist_id):
        try:
            data = request.get_json()
            new_title = data.get('title')

            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()

            playlist = Playlist.query.filter_by(id=playlist_id, user_id=current_user.id).first()
            if not playlist:
                return jsonify({'message': 'Playlist not found'}), 404

            playlist.title = new_title
            db.session.commit()

            return playlist, 200
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({'message': 'An error occurred while updating the playlist'}), 500


    @jwt_required()
    def delete(self, playlist_id):
        try:
            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()
            playlist = Playlist.query.filter_by(id=playlist_id, user_id=current_user.id).first()
            if not playlist:
                return jsonify({'message': 'Playlist not found'}), 404

            db.session.delete(playlist)
            db.session.commit()

            return {'message': 'Playlist deleted successfully'}, 200
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({'message': 'An error occurred while deleting the playlist'}), 500

class PlaylistAddSongResource(Resource):
    @jwt_required()
    @marshal_with(playlist_fields)
    def post(self, playlist_id):
        try:
            playlist = Playlist.query.get(playlist_id)
            if not playlist:
                return jsonify({'message': 'Playlist not found'}), 404

            data = request.get_json()
            song_id = data.get('song_id')
            song = Song.query.get(song_id)
            if not song:
                return jsonify({'message': 'Song not found'}), 404

            playlist.songs.append(song)
            db.session.commit()

            return playlist, 200
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({'message': 'An error occurred while adding a song to the playlist'}), 500

class PlaylistDeleteSongResource(Resource):
    @jwt_required()
    @marshal_with(playlist_fields)
    def delete(self, playlist_id, song_id):
        try:
            playlist = Playlist.query.get(playlist_id)
            if not playlist:
                return jsonify({'message': 'Playlist not found'}), 404

            song = Song.query.get(song_id)
            if not song:
                return jsonify({'message': 'Song not found'}), 404

            if song not in playlist.songs:
                return jsonify({'message': 'Song not in playlist'}), 404

            playlist.songs.remove(song)
            db.session.commit()

            return playlist, 200
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({'message': 'An error occurred while deleting the song from the playlist'}), 500

api.add_resource(PlaylistListResource, '/playlists')
api.add_resource(PlaylistResource, '/playlists/<int:playlist_id>')
api.add_resource(PlaylistAddSongResource, '/playlists/<int:playlist_id>/add-song')
api.add_resource(PlaylistDeleteSongResource, '/playlists/<int:playlist_id>/delete-song/<int:song_id>')
