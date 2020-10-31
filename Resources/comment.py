from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, jwt_optional, fresh_jwt_required
from Models.comment import CommentModel


class Comment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('comment',
                        type=str,
                        required=True,
                        help="Every comment needs a comment."
                        )

    # @jwt_required  # No longer needs brackets
    def get(self, name):
        comment = CommentModel.find_by_name(name)
        if comment:
            return comment.json()
        return {'message': 'comment not found'}, 404

    @jwt_required
    def post(self, name):
        data = Comment.parser.parse_args()

        comment = CommentModel(name, **data)

        try:
            comment.save_to_db()
        except:
            return {"message": "An error occurred inserting the comment."}, 500

        return comment.json(), 201

    # @jwt_required
    # def delete(self, name):
    #     claims = get_jwt_claims()
    #     if not claims['is_admin']:
    #         return {'message': 'Admin privilege required.'}, 401

    #     item = ItemModel.find_by_name(name)
    #     if item:
    #         item.delete_from_db()
    #         return {'message': 'Item deleted.'}
    #     return {'message': 'Item not found.'}, 404

    # def put(self, name):
    #     data = Comment.parser.parse_args()

    #     item = ItemModel.find_by_name(name)

    #     if item:
    #         item.price = data['price']
    #     else:
    #         item = ItemModel(name, **data)

    #     item.save_to_db()

    #     return item.json()


class CommentList(Resource):
    # @jwt_optional
    def get(self):
        """
        Here we get the JWT identity, and then if the user is logged in (we were able to get an identity)
        we return the entire item list.

        Otherwise we just return the item names.

        This could be done with e.g. see orders that have been placed, but not see details about the orders
        unless the user has logged in.
        """
        comments = [comment.json() for comment in CommentModel.find_all()]
        return {'comments': comments}, 200
        # user_id = get_jwt_identity()
        # items = [item.json() for item in ItemModel.find_all()]
        # if user_id:
        #     return {'items': items}, 200
        # return {
        #     'items': [item['name'] for item in items],
        #     'message': 'More data available if you log in.'
        # }, 200
