from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from blacklist import BLACKLIST
from Resources.comment import Comment, CommentList
from Resources.reply import Reply, ReplyList
from Resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
# allow blacklisting for access and refresh tokens
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# could do app.config['JWT_SECRET_KEY'] if we prefer
app.secret_key = 'sandeep'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    # Here we blacklist particular JWTs that have been created in the past.
    return decrypted_token['jti'] in BLACKLIST


api.add_resource(Comment, '/comment/<string:name>')
api.add_resource(CommentList, '/comments')
api.add_resource(Reply, '/reply/<string:comment_id>')
api.add_resource(ReplyList, '/replies')
# api.add_resource(Item, '/item/<string:name>')
# api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
# api.add_resource(TokenRefresh, '/refresh')
# api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
