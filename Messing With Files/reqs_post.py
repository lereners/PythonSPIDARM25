# io_examples/reqs_post.py
import requests, pprint
url = 'https://httpbin.org/post'
data = dict(title='Learn Python Programming')
resp = requests.post(url, data=data)
print('Response for POST')
pprint.pprint(resp.json(),width=-1)
print("-" * 80)
print(resp.json()) # non pretty version