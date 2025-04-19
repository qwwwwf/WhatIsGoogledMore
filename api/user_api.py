from flask import jsonify
from flask_restful import Resource, reqparse, abort

from flask_login import current_user

from config import STAR_EXCHANGE_RATE
from data import db_session
from data.user_model import User

parser = reqparse.RequestParser()


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('username', 'stars', 'points', 'games'))})

    def post(self, user_id, action):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()

        match action:
            case 'exchange-points':
                if current_user.points < STAR_EXCHANGE_RATE:
                    return abort(400, message='Points value should be more 0')

                stars_price = ((current_user.points // STAR_EXCHANGE_RATE) * STAR_EXCHANGE_RATE)
                session.query(User).filter(User.id == user_id).update({
                    'stars': User.stars + (current_user.points // STAR_EXCHANGE_RATE),
                    'points': User.points - stars_price,
                    'points_spent': User.points_spent + stars_price
                })
                session.commit()
                return jsonify({'success': 'OK'})

        abort(404, message='Unknown error')

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})
