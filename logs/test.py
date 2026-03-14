import requests

url = "http://localhost:8000/v1/attendance"
files = {"image": open(r"E:\face.jpeg", "rb")}
data = {"device_id": "device-01"}

res = requests.post(url, data=data, files=files)
print(res.status_code, res.text)
