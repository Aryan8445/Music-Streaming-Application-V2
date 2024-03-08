from flask_restful import Api, Resource, reqparse
from app.models import *
from app.extensions import db

api = Api(prefix='/api')


parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='title should be a string')
parser.add_argument('artist_id', type=int, help='artist_id should be an integer')
parser.add_argument('album_id', type=str, help='album_title should be a string')
parser.add_argument('release_date', help='release date should be a string')
parser.add_argument('genre', type=str, help='genre should be a string')
parser.add_argument('lyrics', type=str, help='lyrics should be a string')
parser.add_argument('file_path', type=str, help='song_file should be a string')



class SongApi(Resource):
    def get(self):
        return 200
    def post(self):
        args = parser.parse_args()
        song = Song(**args)
        db.session.add(song)
        try:
            db.session.commit()
            return {"message": "Song created successfully."}, 201
        except Exception as e:
            return {"message": f"Error creating song: {e}"}, 500




api.add_resource(SongApi, "/song")
