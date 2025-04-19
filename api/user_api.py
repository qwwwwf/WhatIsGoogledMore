import datetime

from flask import jsonify
from flask_restful import Resource, reqparse, abort

from flask_login import current_user
from sqlalchemy.orm.attributes import flag_modified

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

                stars_gave = current_user.points // STAR_EXCHANGE_RATE
                stars_price = ((current_user.points // STAR_EXCHANGE_RATE) * STAR_EXCHANGE_RATE)

                user = session.query(User).get(user_id)
                user.stars += stars_gave
                user.points -= stars_price
                user.points_spent += stars_price

                current_history = user.exchange_history['exchanges']
                current_history.append({
                    'stars_gave': stars_gave,
                    'points_spent': stars_price,
                    'created_at': str(datetime.datetime.now())
                })

                user.exchange_history = {'exchanges': current_history}
                flag_modified(user, 'exchange_history')
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
