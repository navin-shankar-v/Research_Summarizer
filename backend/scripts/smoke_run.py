
import requests, json

payload = {"query":"federated learning in healthcare","n_papers":6,"sources":["arxiv"]}
r = requests.post("http://localhost:8000/api/summarize", json=payload, timeout=120)
print(r.status_code)
print(json.dumps(r.json(), indent=2)[:4000])
