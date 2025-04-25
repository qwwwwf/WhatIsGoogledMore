import random

from flask import jsonify
from flask_restful import Resource
from misc.functions import get_trends


class TrendResource(Resource):
    def get(self):
        trends = get_trends()
        random_trend = random.choice(list(trends.keys()))
        random_trends = random.sample(trends[random_trend], 2)

        data = {
            1: random_trends[0],
            2: random_trends[1]
        }

        return jsonify(data)
