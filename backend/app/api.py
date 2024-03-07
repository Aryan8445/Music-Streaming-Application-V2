from flask_restful import Api, Resource
from app.models import Song
api = Api(prefix='/api')

class SongApi(Resource):
    # def get(self, song_id):
    #     song = Song.query.get(song_id)
    #     return (f"The song : {song} is from API")
    
    def get(self):
        songs = Song.query.all()
        return songs
api.add_resource(SongApi,"/song")