from flask import jsonify, Blueprint, request
from flask_restful import Resource, reqparse, marshal_with, fields, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Playlist, User, Song, db

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

playlist_parser = reqparse.RequestParser()
playlist_parser.add_argument('title', type=str, required=True, help='Title is required')

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
        'artist': fields.String(attribute=lambda x: f"{x.artist.firstname} {x.artist.lastname}")
    }))
}

class PlaylistListResource(Resource):
    @jwt_required()
    @marshal_with(playlist_fields)
    def get(self):
        playlists = Playlist.query.all()
        return playlists

    @jwt_required()
    @marshal_with(playlist_fields)
    def post(self):
        args = playlist_parser.parse_args()
        title = args['title']

        current_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=current_user_email).first()

        new_playlist = Playlist(title=title, user=current_user)
        db.session.add(new_playlist)
        db.session.commit()

        return new_playlist, 201

class PlaylistResource(Resource):
    @jwt_required()
    @marshal_with(playlist_fields)
    def delete(self, playlist_id):
        current_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=current_user_email).first()

        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return {'message': 'Playlist not found'}, 404

        # Check if the current user is the owner of the playlist
        if playlist.user != current_user:
            return {'message': 'Unauthorized'}, 401

        db.session.delete(playlist)
        db.session.commit()

        return {'message': 'Playlist deleted successfully'}, 200

api.add_resource(PlaylistListResource, '/playlists')
api.add_resource(PlaylistResource, '/playlists/<int:playlist_id>')
