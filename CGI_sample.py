import json
import requests


host = '192.168.1.201'
base_url = 'http://{}/pandar.cgi?'.format(host)
get_p = {'action': 'get',
         'object': 'lidar_config'}
response = requests.get(base_url, get_p)
r = json.loads(response.text)
print(r)
spin_speed = {'2': '600rpm', '3': '1200rpm'}[r['Body']['SpinSpeed']]
print(spin_speed)

