from flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest, REGISTRY, start_http_server, CollectorRegistry, multiprocess

app = Flask(__name__)

# Define a counter metric
request_counter = Counter('my_microservice_requests_total', 'Total number of requests received')

@app.route('/process_data', methods=['POST'])
def process_data():
    # Increment the request counter
    request_counter.inc()

    # Get data from the request
    data = request.get_json()
    sum = 0
    for key, value in data.items():
        # Process the values (you can add your business logic here)
        sum += value

    data["sum"] = sum
    # Process the data (you can add your business logic here)
    result = {'message': 'Data received successfully', 'data': data}

    return jsonify(result)

@app.route('/metrics', methods=['GET'])
def metrics():
    # Expose the metrics for Prometheus to scrape
    # registry = CollectorRegistry()
    # multiprocess.MultiProcessCollector(registry)
    # data = generate_latest(request_counter, registry=registry)
    data = generate_latest(request_counter)

    return data

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(9090)

    # Run the Flask app
    app.run(debug=True, port=5000)