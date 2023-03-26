import simpy_search
import json
from flask import Flask, request
import os
from dotenv import load_dotenv
load_dotenv()

CODE = str(os.getenv('CODE'))

app = Flask(__name__)

searcher = simpy_search.Searcher([])  # Default Value

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def index():
    return 'Simpy Search API'

@app.route('/search')
def search():

    try:
        query = request.args.get('q', default='', type=str)
        max_results = request.args.get(
            'max_results', default=searcher.max_results, type=int)

        def check_str_as_bool(v): return v.lower() == 'true'

        basic_search = request.args.get(
            'basic_search', default=searcher.basic_search, type=check_str_as_bool)
        fuzzy_search = request.args.get(
            'fuzzy_search', default=searcher.fuzzy_search, type=check_str_as_bool)
        key_value_pairs = request.args.get(
            'key_value_pairs', default=searcher.key_value_pairs, type=check_str_as_bool)

        searcher.update_parameters(
            max_results, basic_search, fuzzy_search, key_value_pairs)
        results = searcher.search(query)
        searcher.reset_parameters()

        return {'results': results}
    except:
        return {'message': 'Bad request.'}, 400


@app.route('/update_data', methods=['POST'])
def update_data():

    try:
        data = json.loads(request.data)
        code = data['code']
        data_value = data['data']

        if code == CODE:
            if isinstance(data_value, list):
                try:
                    searcher.data = data_value
                    return {'message': 'Data updated successfully.'}, 200
                except Exception as e:
                    print(e)
                    return {'message': 'Unable to update data.'}, 400
            else:
                return {'message': 'Invalid data format.'}, 400
        else:
            return {'message': 'Unauthorized.'}, 401
    except Exception as e:
        print(e)
        return {'message': 'Bad request.'}, 400


if __name__ == '__main__':
    app.run()
