from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Rating, Song, User

api_bp = Blueprint('Rating_api', __name__)
api = Api(api_bp)

rating_parser = reqparse.RequestParser()
rating_parser.add_argument('value', type=int, required=True, help='Rating value is required')

rating_fields = {
    'id': fields.Integer,
    'user_id':fields.Integer,
    'song_id':fields.Integer,
    'value':fields.Integer,

}
class SongRatingsResource(Resource):
    @jwt_required
    @marshal_with(rating_fields)
    def get(self, song_id):
        try:
            song = Song.query.get(song_id)
            if not song:
                return jsonify({'message': 'Song not found'}), 404

            ratings = Rating.query.filter_by(song_id=song_id).all()
            if not ratings:
                return jsonify({'message': 'No ratings found for this song'}), 404

            # Calculate the average rating
            total_ratings = len(ratings)
            total_value = sum(rating.value for rating in ratings)
            average_rating = total_value / total_ratings

            # Format the ratings data
            ratings_data = [{'user_id': rating.user_id, 'value': rating.value} for rating in ratings]

            return jsonify({'song_id': song_id, 'ratings': ratings_data, 'average_rating': average_rating}), 200
        except Exception as e:
            return jsonify({'message': 'An error occurred while fetching ratings'}), 500

    @jwt_required()
    @marshal_with(rating_fields)
    def post(self, song_id):
        try:
            user_id = get_jwt_identity()
            rating_value = request.json.get('value')
            song = Song.query.get(song_id)
            if not song:
                return jsonify({'message': 'Song not found'}), 404

            # Check if the user has already rated the song
            existing_rating = Rating.query.filter_by(user_id=user_id, song_id=song_id).first()
            if existing_rating:
                # Update the existing rating
                existing_rating.value = rating_value
            else:
                # Create a new rating
                new_rating = Rating(user_id=user_id, song_id=song_id, value=rating_value)
                db.session.add(new_rating)

            db.session.commit()

            return jsonify({'message': 'Rating added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'An error occurred while adding or updating the rating'}), 500


api.add_resource(SongRatingsResource, '/songs/<int:song_id>/ratings')
