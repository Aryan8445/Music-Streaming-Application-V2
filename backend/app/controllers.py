from flask import Blueprint, render_template, redirect, request, flash, url_for, jsonify
from flask import current_app as app
from .models import *
from datetime import datetime
from . import db
from sqlalchemy import or_, desc, distinct
from werkzeug.utils import secure_filename
import os


controllers = Blueprint('controllers',__name__)


@controllers.route('/', methods=['GET'])
def index():
    return "success", 200


@controllers.route('/home', methods=['GET'])
def home_api():
    recommended_songs = [song.serialize() for song in Song.query.order_by(Song.upload_date.desc()).limit(5).all()]
    # user_playlists = [playlist.serialize() for playlist in Playlist.query.filter_by(user_id=current_user.id).limit(4).all()]
    albums = [album.serialize() for album in Album.query.limit(4).all()]
    rock_songs = [song.serialize() for song in Song.query.filter_by(genre='Rock').all()]
    Bhakti_songs = [song.serialize() for song in Song.query.filter_by(genre='Bhakti').all()]

    return jsonify(recommended_songs=recommended_songs, albums=albums, rock_songs=rock_songs, Bhakti_songs=Bhakti_songs)
