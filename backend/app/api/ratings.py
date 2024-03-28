from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Song, Rating, User, db

api_bp = Blueprint('rating_api', __name__)
api = Api(api_bp)

rating_parser = reqparse.RequestParser()
rating_parser.add_argument('value', type=int, required=True, help='Rating value is required')

rating_fields = {
    'average_rating': fields.Float,
    'total_ratings': fields.Integer
}

class RatingResource(Resource):
    @jwt_required()
    @marshal_with(rating_fields)
    def post(self, song_id):
        args = rating_parser.parse_args()
        rating_value = args['value']

        current_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=current_user_email).first()

        if not current_user:
            return {'message': 'User not found'}, 404

        song = Song.query.get(song_id)
        if not song:
            return {'message': 'Song not found'}, 404

        if not (1 <= rating_value <= 5):
            return {'message': 'Invalid rating value. Rating value must be an integer between 1 and 5'}, 400

        # Check if the user has already rated this song
        existing_rating = Rating.query.filter_by(user_id=current_user.id, song_id=song_id).first()
        if existing_rating:
            # Update the existing rating
            existing_rating.value = rating_value
        else:
            # Create a new rating
            new_rating = Rating(value=rating_value, user_id=current_user.id, song_id=song_id)
            db.session.add(new_rating)

        db.session.commit()

        # Calculate average rating and total ratings for the song
        ratings = Rating.query.filter_by(song_id=song_id).all()
        total_ratings = len(ratings)
        if total_ratings == 0:
            return {'average_rating': 0.0, 'total_ratings': 0}

        average_rating = sum([rating.value for rating in ratings]) / total_ratings
        return {'average_rating': average_rating, 'total_ratings': total_ratings}, 201

    @jwt_required()
    @marshal_with(rating_fields)
    def get(self, song_id):
        song = Song.query.get(song_id)
        if not song:
            return {'message': 'Song not found'}, 404

        ratings = Rating.query.filter_by(song_id=song_id).all()
        total_ratings = len(ratings)
        if total_ratings == 0:
            return {'average_rating': 0.0, 'total_ratings': 0}

        average_rating = sum([rating.value for rating in ratings]) / total_ratings
        return {'average_rating': average_rating, 'total_ratings': total_ratings}

api.add_resource(RatingResource, '/songs/<int:song_id>/ratings')
