from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, jwt_optional, fresh_jwt_required
from Models.reply import ReplyModel
from Models.comment import CommentModel


class Reply(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('reply',
                        type=str,
                        required=False,
                        help="Every reply needs a reply."
                        )
    parser.add_argument('reply_type',
                        type=str,
                        required=True,
                        help="Every reply needs a reply type like L, D, R."
                        )
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Every reply needs a name who replied"
                        )
    parser.add_argument('parent_reply_id',
                        type=str,
                        required=False,
                        help="parent_reply_id is required for replying to parent"
                        )

    # @jwt_required  # No longer needs brackets
    def get(self, name):
        reply = ReplyModel.find_by_name(name)
        if reply:
            return reply.json()
        return {'message': 'reply not found'}, 404

    @jwt_required
    def post(self, comment_id):
        data = Reply.parser.parse_args()
        # if(comment_id in ReplyModel.find_all().map(lambda x:x))
        comment_data = CommentModel.find_by_comment_id(comment_id)
        if(comment_data):
            if(data.parent_reply_id):
                print(data.parent_reply_id)
                parent_reply_data = ReplyModel.find_by_reply_id(
                    data.parent_reply_id)
                if(parent_reply_data):
                    reply = ReplyModel(comment_id, **data)
                    try:
                        reply.save_to_db()
                    except:
                        return {"message": "An error occurred inserting the reply."}, 500
                    return reply.json(), 201
                else:
                    return {'message': 'parent reply id for the reply is not present'}, 401

            reply = ReplyModel(comment_id, **data)
            try:
                reply.save_to_db()
            except:
                return {"message": "An error occurred inserting the reply."}, 500

            return reply.json(), 201
        else:
            return {'message': 'comment id for the reply is not present'}, 401

    @jwt_required
    def delete(self, comment_id):
        reply_id = comment_id
        # here comment id is the reply id to be deleted

        # if(comment_id in ReplyModel.find_all().map(lambda x:x))
        reply_data = ReplyModel.find_by_reply_id(reply_id)
        if(reply_data):
            all_replies_for_the_parent_reply_id = ReplyModel.find_all_reply_id_using_parent_id(
                reply_id)
            if(len(all_replies_for_the_parent_reply_id) > 0):
                try:
                    [reply_data.delete_from_db()
                     for reply_data in all_replies_for_the_parent_reply_id]
                except:
                    return {"message": "An error occurred when deleting child for parent reply id"}, 500
            print(all_replies_for_the_parent_reply_id)
            try:
                reply_data.delete_from_db()
                return {'message': 'Item deleted.'}
            except:
                return {"message": "An error occurred when deleting the reply."}, 500
        else:
            return {'message': 'reply id not found'}, 404


class ReplyList(Resource):
    # @jwt_optional
    def get(self):
        """
        Here we get the JWT identity, and then if the user is logged in (we were able to get an identity)
        we return the entire item list.

        Otherwise we just return the item names.

        This could be done with e.g. see orders that have been placed, but not see details about the orders
        unless the user has logged in.
        """
        replies = [reply.json() for reply in ReplyModel.find_all()]
        return {'replies': replies}, 200
