import json
from flask.ext.negotiate import produces
from flask import Flask, request
from compute import Compute

api = Flask(__name__)

@produces('application/json')
@api.route('/cloudpi', methods=['GET'])
def entry_point():
    if 'input' not in request.args:
            raise Exception({'message': 'query parameter {0} not provided.'.format('input')})

    compute = Compute(request.args['input'])

    # computed_pi = compute.run_pifft()

    return json.dumps('computed_pi'), 200, None


def main():
    api.run(host='0.0.0.0', debug=False)