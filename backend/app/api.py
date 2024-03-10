from flask_restful import Api, Resource, reqparse
from flask import jsonify, request
from app.models import *
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Api(prefix='/api')

class SongApi(Resource):
    @jwt_required()
    def post(self):
        # Get the current user's identity from the JWT token
        current_user_email = get_jwt_identity()

        # Check if the current user exists in the database
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return jsonify({'message': 'User not found'}), 404

        # Define parser to parse the request data
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('release_date', type=str, required=True, help='Release date is required')
        parser.add_argument('genre', type=str, required=True, help='Genre is required')
        parser.add_argument('file_path', type=str, required=True, help='File path is required')
        parser.add_argument('album_id', type=int)
        parser.add_argument('lyrics', type=str)
        
        # Parse the request data
        data = parser.parse_args()
        
        # Create a new Song object
        new_song = Song(
            title=data['title'],
            artist_id=current_user.id,
            release_date=datetime.strptime(data['release_date'], '%Y-%m-%d').date(),
            genre=data['genre'],
            album_id=data['album_id'],
            file_path=data['file_path'],
            lyrics=data['lyrics']
        )
        
        # Save the new song to the database
        try:
            new_song.save()
            return jsonify({'message': 'Song uploaded successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500


api.add_resource(SongApi, "/song")
