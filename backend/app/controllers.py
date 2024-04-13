from flask import Blueprint, send_file
from flask_restful import Resource, Api, marshal, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Song, Rating, User, Album, Admin, db
from sqlalchemy import desc, func
import matplotlib.pyplot as plt
import io


controllers = Blueprint('controllers',__name__)
api = Api(controllers)

@controllers.route('/', methods=['GET'])
def index():
    return "success", 200


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
            # Get the email of the current user from JWT identity
            current_user_email = get_jwt_identity()

            # Find the user based on the email
            user = User.query.filter_by(email=current_user_email).first()

            if not user:
                return {'message': 'User not found'}, 404

            # Fetch total songs uploaded by the creator
            total_songs_uploaded = Song.query.filter_by(artist_id=user.id).count()

            # Fetch total albums created by the creator
            total_albums = Album.query.filter_by(artist_id=user.id).count()

            # Fetch all songs uploaded by the creator
            songs = Song.query.filter_by(artist_id=user.id).all()

            # Fetch all albums created by the creator
            all_albums = Album.query.filter_by(artist_id=user.id).all()

            # Fetch all ratings for the creator's songs
            all_ratings = Rating.query.join(Song).filter(Song.artist_id == user.id).all()

            # Calculate total ratings and average rating
            total_ratings = sum([rating.value for rating in all_ratings])
            average_rating = round(total_ratings / len(all_ratings) if len(all_ratings) > 0 else 0, 2)

            # Prepare the response data
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
            # Get the email of the current user from JWT identity
            current_user_email = get_jwt_identity()

            # Find the user based on the email
            admin = Admin.query.filter_by(email=current_user_email).first()

            if not admin:
                return {'message': 'Admin not found'}, 404

            # Fetch total songs uploaded by the creator
            total_normal_users = User.query.filter_by(user_type='user').count()
            total_creators = User.query.filter_by(user_type='creator').count()
            total_songs = Song.query.count()
            total_albums = Album.query.count()
            total_genres = Song.query.group_by(Song.genre).count()
            top_rated_songs = (Song.query.join(Rating).group_by(Song.id).order_by(desc(func.avg(Rating.value))).limit(10).all())

            # Prepare the response data
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
            # Fetch all users with user type 'creator'
            creators = User.query.filter_by(user_type='creator').all()

            # Prepare the response data
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
            # Fetch all users with user type 'user'
            users = User.query.filter_by(user_type='user').all()

            # Prepare the response data
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

api.add_resource(BlacklistUserResource, '/users/<int:user_id>/blacklist')
api.add_resource(CreatorDashboardResource, '/creator-dashboard')
api.add_resource(AdminDashboardResource, '/admin-dashboard')
api.add_resource(CreatorListResource, '/creators')
api.add_resource(UserListResource, '/users')
