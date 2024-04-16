from flask import Blueprint, send_file
from flask_restful import Resource, Api, marshal, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Song, Rating, User, Album, Admin, db
from sqlalchemy import desc, func
import matplotlib.pyplot as plt
import io
from app.caching import cache

controllers = Blueprint('controllers',__name__)
api = Api(controllers)




song_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'release_date': fields.DateTime(dt_format='iso8601'),
    'genre': fields.String,
    'file_path': fields.String,
    'lyrics': fields.String,
    'upload_date': fields.DateTime(dt_format='iso8601'),
    'artist': fields.String(attribute=lambda x: f"{x.artist.firstname} {x.artist.lastname}"),
}

album_fields = {
    'id': fields.Integer,
    'title': fields.String,
}

class CreatorDashboardResource(Resource):
    @jwt_required()
    def get(self):
        try:

            current_user_email = get_jwt_identity()

            user = User.query.filter_by(email=current_user_email).first()

            if not user:
                return {'message': 'User not found'}, 404

            total_songs_uploaded = Song.query.filter_by(artist_id=user.id).count()

            total_albums = Album.query.filter_by(artist_id=user.id).count()

            songs = Song.query.filter_by(artist_id=user.id).all()

            all_albums = Album.query.filter_by(artist_id=user.id).all()

            all_ratings = Rating.query.join(Song).filter(Song.artist_id == user.id).all()

            total_ratings = sum([rating.value for rating in all_ratings])
            average_rating = round(total_ratings / len(all_ratings) if len(all_ratings) > 0 else 0, 2)

            response_data = {
                'artist_id': user.id,
                'artist_firstname':user.firstname,
                'artist_lastname':user.lastname,
                'artist_email': user.email,
                'total_songs_uploaded': total_songs_uploaded,
                'total_albums': total_albums,
                'average_rating': average_rating,
                'songs': [marshal(song, song_fields) for song in songs],
                'albums': [marshal(album, album_fields) for album in all_albums]
            }

            return response_data, 200

        except Exception as e:
            return {'error': str(e)}, 500

class AdminDashboardResource(Resource):
    @jwt_required()
    def get(self):
        try:

            current_user_email = get_jwt_identity()

            admin = Admin.query.filter_by(email=current_user_email).first()

            if not admin:
                return {'message': 'Admin not found'}, 404

            total_normal_users = User.query.filter_by(user_type='user').count()
            total_creators = User.query.filter_by(user_type='creator').count()
            total_songs = Song.query.count()
            total_albums = Album.query.count()
            total_genres = Song.query.group_by(Song.genre).count()
            top_rated_songs = (Song.query.join(Rating).group_by(Song.id).order_by(desc(func.avg(Rating.value))).limit(10).all())

            response_data = {
                'total_normal_user': total_normal_users,
                'total_creators': total_creators,
                'total_songs': total_songs,
                'total_albums': total_albums,
                'total_genres': total_genres,
                'top_rated_songs': [marshal(song, song_fields) for song in top_rated_songs]
            }

            return response_data, 200

        except Exception as e:
            return {'error': str(e)}, 500

class CreatorListResource(Resource):
    @jwt_required()
    def get(self):
        try:

            creators = User.query.filter_by(user_type='creator').all()


            response_data = {
                'creators': [{
                    'id': creator.id,
                    'firstname': creator.firstname,
                    'lastname': creator.lastname,
                    'email': creator.email,
                    'is_blacklisted': creator.is_blacklisted,
                } for creator in creators]
            }

            return response_data, 200

        except Exception as e:
            return {'error': str(e)}, 500

class UserListResource(Resource):
    @jwt_required()
    def get(self):
        try:

            users = User.query.filter_by(user_type='user').all()

            response_data = {
                'users': [{
                    'id': user.id,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'email': user.email,
                    'is_blacklisted': user.is_blacklisted,
                } for user in users]
            }

            return response_data, 200

        except Exception as e:
            return {'error': str(e)}, 500

class BlacklistUserResource(Resource):
    @jwt_required()
    def post(self, user_id):
        try:
            # Get the email of the current user from JWT identity
            current_user_email = get_jwt_identity()

            # Find the admin based on the email
            admin = Admin.query.filter_by(email=current_user_email).first()

            if not admin:
                return {'message': 'Admin not found'}, 404

            # Find the user to be blacklisted/whitelisted
            user = User.query.get(user_id)

            if not user:
                return {'message': 'User not found'}, 404

            # Check if the user is already blacklisted
            if user.is_blacklisted:
                return {'message': 'User is already blacklisted'}, 400

            # Blacklist the user
            user.is_blacklisted = True
            db.session.commit()

            return {'message': 'User blacklisted successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @jwt_required()
    def delete(self, user_id):
        try:
            # Get the email of the current user from JWT identity
            current_user_email = get_jwt_identity()

            # Find the admin based on the email
            admin = Admin.query.filter_by(email=current_user_email).first()

            if not admin:
                return {'message': 'Admin not found'}, 404

            # Find the user to be removed from blacklist
            user = User.query.get(user_id)

            if not user:
                return {'message': 'User not found'}, 404

            # Check if the user is not blacklisted
            if not user.is_blacklisted:
                return {'message': 'User is not blacklisted'}, 400

            # Remove the user from blacklist
            user.is_blacklisted = False
            db.session.commit()

            return {'message': 'User removed from blacklist successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class FlagSongResource(Resource):
    @jwt_required()
    def post(self, song_id):
        try:
            # Get the email of the current user from JWT identity
            current_user_email = get_jwt_identity()

            # Find the admin based on the email
            admin = Admin.query.filter_by(email=current_user_email).first()

            if not admin:
                return {'message': 'Admin not found'}, 404

            # Find the song to be flagged
            song = Song.query.get(song_id)

            if not song:
                return {'message': 'Song not found'}, 404

            # Check if the song is already flagged
            if song.is_flagged:
                return {'message': 'Song is already flagged'}, 400

            # Flag the song
            song.is_flagged = True
            db.session.commit()
            cache.clear()


            return {'message': 'Song flagged successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @jwt_required()
    def delete(self, song_id):
        try:
            # Get the email of the current user from JWT identity
            current_user_email = get_jwt_identity()

            # Find the admin based on the email
            admin = Admin.query.filter_by(email=current_user_email).first()

            if not admin:
                return {'message': 'Admin not found'}, 404

            # Find the song to be unflagged
            song = Song.query.get(song_id)

            if not song:
                return {'message': 'Song not found'}, 404

            # Check if the song is not flagged
            if not song.is_flagged:
                return {'message': 'Song is not flagged'}, 400

            # Unflag the song
            song.is_flagged = False
            db.session.commit()

            return {'message': 'Song unflagged successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


api.add_resource(BlacklistUserResource, '/users/<int:user_id>/blacklist')
api.add_resource(CreatorDashboardResource, '/creator-dashboard')
api.add_resource(FlagSongResource, '/songs/<int:song_id>/flag')
api.add_resource(AdminDashboardResource, '/admin-dashboard')
api.add_resource(CreatorListResource, '/creators')
api.add_resource(UserListResource, '/users')



