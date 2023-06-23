import simpy_search
import json
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Simpy Search API'


@app.route('/search', methods=['POST'])
def search():
    try:
        searcher = simpy_search.Searcher([])
        try:
            data = json.loads(request.data)
            data_value = data['data']
            if isinstance(data_value, list):

                searcher.data = data_value
            else:
                return {'message': 'Invalid data format.'}, 400
        except Exception:
            return {'message': 'Bad request.'}, 400

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


if __name__ == '__main__':
    app.run()
