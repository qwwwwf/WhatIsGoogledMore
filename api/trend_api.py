import json
import random

from flask import jsonify
from flask_restful import Resource, reqparse

from data import db_session
from data.game_model import Game
from data.user_model import User
from misc.functions import get_trends
from flask_login import current_user

parser = reqparse.RequestParser()
parser.add_argument('stats', required=True)

trends = get_trends()


class TrendResource(Resource):
    def get(self):
        random_trend_year = random.choice(list(trends.keys()))
        random_trend_category = random.choice(list(trends[random_trend_year].keys()))
        random_trends = random.sample(trends[random_trend_year][random_trend_category], 2)

        data = {
            '1': random_trends[0],
            '2': random_trends[1],
            'year': random_trend_year,
            'category': random_trend_category,
            'correct': 'trend-1' if int(random_trends[0][0]) < int(random_trends[1][0]) else 'trend-2'
        }

        return jsonify(data)

    def post(self):
        args = parser.parse_args()
        stats = json.loads(args['stats'].replace('\'', '"'))

        trends = stats['trends']
        points_gave = stats['points_gave']

        session = db_session.create_session()

        user = session.query(User).get(current_user.id)
        game = Game(
            total_rounds=len(trends) + 1,
            trends=trends,
            points_gave=points_gave,
            user_id=current_user.id
        )

        session.add(game)
        user.points += points_gave

        session.commit()

        return jsonify({'status': 'ok'})
