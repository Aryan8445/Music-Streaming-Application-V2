from app.models import *
from app.caching import cache

def is_allowed_img(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def is_allowed_txt(filename):
    allowed_extensions = {'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def is_allowed_song(filename):
    allowed_extensions = {'mp3', 'wav', 'flac', 'aac'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@cache.memoize()
def get_all_users():
    users = User.query.all()
    return users


def find_user(email):
    user = User.query.filter_by(email=email).first()
    return user


def find_admin(email):
    user = Admin.query.filter_by(email=email).first()
    return user

@cache.memoize()
def get_songs_all():
    songs = Song.query.order_by(Song.id.desc()).all()
    return songs

@cache.memoize()
def find_song_by_id(id):
    song = Song.query.filter_by(id == id).first()
    return song


# @cache.memoize()
# def get_comments_post(post_id):
#     comments = Comment.query.filter_by(post=post_id).order_by(Comment.roll.desc()).all()
#     return comments

# @cache.memoize()
# def get_posts_author(author):
#     posts = Post.query.filter_by(author = author).all()
#     return posts

# @cache.memoize()
# def get_posts_author_desc(author):
#     posts = Post.query.filter_by(author = author).order_by(Post.roll.desc()).all()
#     return posts

# @cache.memoize()
# def get_content_all():
#     posts = db.session.query(Post, User).filter(Post.author==User.username).order_by(Post.roll.desc()).limit(6).all()
#     return posts

# @cache.memoize()
# def get_content_user(follows):
#     posts = db.session.query(Post, User).filter(Post.author==User.username, Post.author.in_(follows)).order_by(Post.roll.desc()).limit(6).all()
#     return posts

# @cache.memoize()
# def get_follows(user):
#     follows = Follow.query.filter(Follow.follower == user).all()
#     return follows

# @cache.memoize()
# def get_followers(user):
#     followers = Follow.query.filter(Follow.following == user).all()
#     return followers

# @cache.memoize()
# def get_follow_status(follower, following):
#     follow = Follow.query.filter(Follow.following == following, Follow.follower == follower).all()
#     return {"status": "true"} if len(follow) > 0 else {"status": "false"}

# @cache.memoize()
# def get_like_status(user, post):
#     like = Likes.query.filter_by(user=user, post=post).first()
#     return like