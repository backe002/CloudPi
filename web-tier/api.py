import json
from flask.ext.negotiate import produces
from flask import Flask, request

api = Flask(__name__)

@produces('application/json')
@api.route('/cloudpi', methods=['GET'])
def entry_point():
    if 'input' not in request.args:
            raise Exception({'message': 'query parameter {0} not provided.'.format('input')})

    pi_to_compute = request.args['input']

    computed_pi = compute.get(pi_to_compute)

    return json.dumps(computed_pi), 200, None


def main():
    api.run(host='0.0.0.0', debug=False)