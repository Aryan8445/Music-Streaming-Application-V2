from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, fields, marshal
from sqlalchemy import or_
from app.models import Song, Album, User

api_bp = Blueprint('Search_api', __name__)
api = Api(api_bp)

song_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'release_date': fields.DateTime(dt_format='iso8601'),
    'genre': fields.String,
    'file_path': fields.String,
    'lyrics': fields.String,
    'artist': fields.String(attribute=lambda x: f"{x.artist.firstname} {x.artist.lastname}"),
}

album_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'artist': fields.String(attribute=lambda x: f"{x.artist.firstname} {x.artist.lastname}"),
}

class SearchResource(Resource):
    def post(self):
        # Access the search query from the JSON data in the request body
        json_data = request.get_json()
        query = json_data.get('query', '')

        # Search for songs and albums matching the query text in the artist name, genre, or title
        songs = Song.query.join(User).filter(
            or_(
                User.firstname.ilike(f"%{query}%"),
                User.lastname.ilike(f"%{query}%"),
                Song.genre.ilike(f"%{query}%"),
                Song.title.ilike(f"%{query}%")
            )
        ).all()

        albums = Album.query.join(User).filter(
            or_(
                User.firstname.ilike(f"%{query}%"),
                User.lastname.ilike(f"%{query}%"),
                Album.title.ilike(f"%{query}%")
            )
        ).all()

        # Serialize the results
        serialized_songs = [marshal(song, song_fields) for song in songs]
        serialized_albums = [marshal(album, album_fields) for album in albums]

        return jsonify({
            'songs': serialized_songs,
            'albums': serialized_albums
        })

api.add_resource(SearchResource, '/search')
