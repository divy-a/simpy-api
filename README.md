# Simpy Search API Documentation

The Simpy Search API is a Flask-based backend application that provides search functionality using the Simpy Search library. It allows users to perform searches and update the search data.

## Getting Started

To get started with the API, follow the steps below:

1. Install the required dependencies by running the following command:
```
pip install flask
```

3. Start the Flask application by running the following command:
```
python app.py
```


The API will be accessible at:
```
http://localhost:5000
```

## API Endpoints

### 1. Index

- **Endpoint:** `/`
- **Method:** GET
- **Description:** Returns a simple message indicating that the Simpy Search API is running.
- **Response:** Returns the string `'Simpy Search API'`.

### 2. Search

- **Endpoint:** `/search`
- **Method:** POST
- **Description:** Performs a search operation based on the provided query and data.
- **Request Body:**
- `data`: The search data to be used. It should be an array of strings.
- **Query Parameters:**
- `q` (optional): The search query string. Default is an empty string.
- `max_results` (optional): The maximum number of search results to return. Default is the maximum defined in the backend.
- `basic_search` (optional): Perform a basic search if `true`, otherwise perform an advanced search. Default is `true`.
- `fuzzy_search` (optional): Enable fuzzy search if `true`, otherwise disable it. Default is `false`.
- `key_value_pairs` (optional): Include key-value pairs in the search results if `true`, otherwise exclude them. Default is `false`.
- **Response:** Returns a JSON object containing the search results.
- `results`: An array of search results matching the query.
 - `index` (optional): The index of the search result.
 - `value` (optional): The value of the search result.
- **Errors:**
- `400 Bad Request`: If the request is malformed or the data format is invalid.

## Error Responses

The API provides error responses in JSON format with the following structure:

```json
{
"message": "Error message"
}
