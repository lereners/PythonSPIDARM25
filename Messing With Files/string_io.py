# io_examples/string_io.py
import io
with io.StringIO() as stream:
    stream.write('Learning Python Programming.\n')
    print('Become a Python ninja!', file=stream)
    contents = stream.getvalue()
    print(contents)
import requests
resp = requests.get('https://httpbin.org/get')
print(resp.json())