from flask import Blueprint, render_template, redirect, request, flash, url_for
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

