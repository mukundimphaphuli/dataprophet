import requests, statistics

base_url = "http://127.0.0.1:5000/signals"

class SignalBatch:
  def __init__(self, id, start, end, batch_size=1000):
    self.id = id
    self.start = start
    self.end = end
    self.batch_size = batch_size

  def __iter__(self):
    self.offset = 0
    return self

  def __next__(self):
    query_params = {
      "start": self.start,
      "end": self.end,
      "page_size": self.batch_size,
      "offset": self.offset
    }
    request = requests.get(base_url + "/" + str(self.id) + "/values", params=query_params)

    batch = request.json()
    if len(batch) != 0:
      self.offset += 1
      return batch
    
    raise StopIteration

def get_signals_data():
  data = []
  signal_list_request = requests.get(base_url)
  for id in signal_list_request.json():
    signal_request = requests.get(base_url + "/" + str(id))
    signal = signal_request.json()
    data.append({
      "id": id,
      "name": signal["name"],
      "group": signal["group"],
    })

  return data

def get_signal_values(start, end, id):
  values = []
  next = True
  offset = 0
  while next:
    query_params = {"start": start, "end": end, "page_size": 1000, "offset": offset}
    request = requests.get(base_url + "/" + str(id) + "/values", params=query_params)

    if request.status_code != 200:
      next = False
      break

    batch = request.json()
    if len(batch) == 0:
      next = False
      break

    offset += 1

    for item in batch:
      values.append(item["value"])

  return values

def mean (start, end, group=None):
  signal_data = get_signals_data()
  data = []
  for item in signal_data:
    values = get_signal_values(start, end, item["id"])

    if len(values) > 0:
      data.append({
        "name": item["name"],
        "mean": statistics.mean(values)
      })

  return data
    

def std (start, end, group=None):
  signal_data = get_signals_data()
  data = []
  for item in signal_data:
    values = get_signal_values(start, end, item["id"])

    if len(values) > 0:
      data.append({
        "name": item["name"],
        "std": statistics.stdev(values)
      })

  return data

def stats (start, end, group=None):
  signal_data = get_signals_data()
  data = []
  for item in signal_data:
    values = get_signal_values(start, end, item["id"])

    if len(values) > 0:
      data.append({
        "name": item["name"],
        "mean": statistics.mean(values),
        "std": statistics.stdev(values)
      })

  return data

def raw (start, end, name, batch_size=1000):
  signal_id = None
  signal_list_request = requests.get(base_url)
  for id in signal_list_request.json():
    signal_request = requests.get(base_url + "/" + str(id))
    signal = signal_request.json()
    if signal["name"] == name:
      signal_id = id
      break

  if signal_id == None:
    raise Exception("Signal provided not found")

  return SignalBatch(signal_id, start, end, batch_size)
