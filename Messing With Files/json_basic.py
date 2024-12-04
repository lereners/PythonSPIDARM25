# json_examples/json_basic.py
import sys
import json
data = {
    'big_number': 2 ** 3141,
    'max_float': sys.float_info.max,
    'a_list': [2, 3, 5, 7],
}
json_data = json.dumps(data)
data_out = json.loads(json_data)
assert data == data_out # json and back, data matches
# test if  True, if not, False raises an AssertionError.
print(f'all output: {data_out} \n')
print('*' * 20, 'divider line','*' * 40 )
print(json.dumps(data, indent=2, sort_keys=True))