from flask import Flask, jsonify, request

data = {
  "d5eda9d1": {
    "id": 1,
    "name": "temperature_celc_1A",
    "group": ["laboratory1", "machineA"],
    "timestamp": "2023-07-11T00:00:00.000Z",
    "value": 123.456
  },
  "d5eda9d2": {
    "id": 1,
    "name": "temperature_celc_1A",
    "group": ["laboratory1", "machineA"],
    "timestamp": "2023-07-12T00:00:00.000Z",
    "value": 105.456
  },
  "d5eda9d3": {
    "id": 1,
    "name": "temperature_celc_1A",
    "group": ["laboratory1", "machineA"],
    "timestamp": "2023-07-13T00:00:00.000Z",
    "value": 113.456
  },
  "d5eda9d4": {
    "id": 1,
    "name": "temperature_celc_1A",
    "group": ["laboratory1", "machineA"],
    "timestamp": "2023-07-14T00:00:00.000Z",
    "value": 130.456
  },
  "d5eda9d5": {
    "id": 1,
    "name": "temperature_celc_1A",
    "group": ["laboratory1", "machineA"],
    "timestamp": "2023-07-15T00:00:00.000Z",
    "value": 120.456
  },
  "d5eda9d6": {
    "id": 1,
    "name": "temperature_celc_1A",
    "group": ["laboratory1", "machineA"],
    "timestamp": "2023-07-16T00:00:00.000Z",
    "value": 103.456
  },
  "ea16aa01fe3f": {
    "id": 2,
    "name": "pressure_kpa_1A",
    "group": ["laboratory1", "machineB"],
    "timestamp": "2023-07-23T00:00:00.000Z",
    "value": 709.0
  },
  "ea16aa01fe4f": {
    "id": 2,
    "name": "pressure_kpa_1A",
    "group": ["laboratory1", "machineB"],
    "timestamp": "2023-07-24T00:00:00.000Z",
    "value": 767.0
  },
  "ea16aa01fe5f": {
    "id": 2,
    "name": "pressure_kpa_1A",
    "group": ["laboratory1", "machineB"],
    "timestamp": "2023-07-25T00:00:00.000Z",
    "value": 739.6
  },
  "ea16aa01fe6f": {
    "id": 2,
    "name": "pressure_kpa_1A",
    "group": ["laboratory1", "machineB"],
    "timestamp": "2023-07-26T00:00:00.000Z",
    "value": 735.04
  },
  "ea16aa01fe7f": {
    "id": 2,
    "name": "pressure_kpa_1A",
    "group": ["laboratory1", "machineB"],
    "timestamp": "2023-07-27T00:00:00.000Z",
    "value": 749.6
  },
  "c0e58dd9": {
    "id": 3,
    "name": "humidity_per_1A",
    "timestamp": "2023-07-11T00:00:00.000Z",
    "value": 76.0
  },
  "c0e58dd2": {
    "id": 3,
    "name": "humidity_per_1A",
    "timestamp": "2023-07-12T00:00:00.000Z",
    "value": 66.0
  },
  "c0e58dd3": {
    "id": 3,
    "name": "humidity_per_1A",
    "timestamp": "2023-07-13T00:00:00.000Z",
    "value": 80.7
  },
  "c0e58dd4": {
    "id": 3,
    "name": "humidity_per_1A",
    "timestamp": "2023-07-14T00:00:00.000Z",
    "value": 73.1
  },
  "c0e58dd5": {
    "id": 3,
    "name": "humidity_per_1A",
    "timestamp": "2023-07-15T00:00:00.000Z",
    "value": 73.9
  },
  "15b682476bf7": {
    "id": 4,
    "name": "height_m_1A",
    "group": [],
    "timestamp": "2023-07-23T00:00:00.000Z",
    "value": 7.8
  },
  "15b682476bf4": {
    "id": 4,
    "name": "height_m_1A",
    "group": [],
    "timestamp": "2023-07-24T00:00:00.000Z",
    "value": 5.8
  },
  "15b682476bf5": {
    "id": 4,
    "name": "height_m_1A",
    "group": [],
    "timestamp": "2023-07-25T00:00:00.000Z",
    "value": 6.5
  },
  "15b682476bf6": {
    "id": 4,
    "name": "height_m_1A",
    "group": [],
    "timestamp": "2023-07-26T00:00:00.000Z",
    "value": 6.0
  }
}

app = Flask(__name__)

@app.route('/signals', methods=['GET'])
def get_signals():
  signals = []
  for item in data.values():
    signals.append(item["id"])

  return jsonify(list(set(signals)))

@app.route('/signals/<int:id>', methods=['GET'])
def get_signal(id: int):
  signal = {}
  for item in data.values():
    if item["id"] == id:
      signal["name"] = item["name"]
      signal["group"] = item.get("group", None)
      break

  return jsonify(signal)

@app.route('/signals/<int:id>/values', methods=['GET'])
def get_signal_values(id: int):
  start = request.args.get('start')
  end = request.args.get('end')
  page_size =int(request.args.get('page_size'))
  offset = int(request.args.get('offset'))

  signals = []
  for item in data.values():
    if item["id"] == id and item["timestamp"] >= start and item["timestamp"] < end:
      signals.append({
        "timestamp": item["timestamp"],
        "value": item["value"]
      })

  skip = page_size * offset
  if skip > len(signals):
    return jsonify([])

  return jsonify(signals[skip:])
