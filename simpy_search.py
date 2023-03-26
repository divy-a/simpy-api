from fuzzywuzzy import fuzz as __fuzz, process as __process


class Searcher():

    def __init__(self, data: list, max_results=10, basic_search=True, fuzzy_search=True, key_value_pairs=True):
        self.data = data
        self.max_results = max_results
        self.basic_search = basic_search
        self.fuzzy_search = fuzzy_search
        self.key_value_pairs = key_value_pairs

    def search(self, query: str):

        search_results = []

        if query == '' or self.max_results <= 0:
            return search_results

        query = query.lower()

        if self.basic_search:
            search_results += basic_search(self.data, query, self.max_results)

        if self.fuzzy_search:
            search_results += fuzzy_search(self.data,
                                           query, self.max_results-len(search_results))

        unique_results = list(dict.fromkeys(search_results))
        
        if self.key_value_pairs:
            return get_key_value_pairs(unique_results, self.data)
        else:
            return unique_results

    def update_parameters(self, max_results=10, basic_search=True, fuzzy_search=True, key_value_pairs=True):
        self.max_results = max_results
        self.basic_search = basic_search
        self.fuzzy_search = fuzzy_search
        self.key_value_pairs = key_value_pairs

    def reset_parameters(self):
        self.update_parameters()

    def update_data(self, data: list):
        self.data = data


def basic_search(data: list, query: str, max_results: int) -> list[int]:

    starts_with_indices = []
    contains_indices = []

    for index, element in enumerate(data):
        if len(starts_with_indices) == max_results:
            break

        element_lower = str(element).lower()

        if element_lower.startswith(query):
            starts_with_indices.append(index)

        elif query in element_lower:
            contains_indices.append(index)

    return (starts_with_indices+contains_indices)[:max_results]


def fuzzy_search(data: list, query: str, max_results: int) -> list[int]:

    if max_results <= 0:
        return []

    fuzzy_indices = []

    fuzzy_search_results = __process.extract(
        query, data, scorer=__fuzz.token_sort_ratio, limit=max_results)

    for element in fuzzy_search_results:
        fuzzy_indices.append(data.index(element[0]))

    return fuzzy_indices


def get_key_value_pairs(indices: list[int], data: list):
    results = []
    for index in indices:
        element = {
            'index': index,
            'value': data[index]
        }
        results.append(element)
    return results


if __name__ == "__main__":
    data = ['apple', 'banana', 'mango', 'cherry', 'orange', 'lemon', 'strawberrie', 'grape',
            'watermelon', 'blueberries', 'jackfruit', 'kiwi', 'Pomegranate', 'Peaches', 'Pears', 'Papaya']
    simpy = Searcher(data)
    results = simpy.search('ago')
    for result in results:
        print(result)
