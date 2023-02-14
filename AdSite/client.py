import requests

BASE_URL = 'http://127.0.0.1:5000/'

response_post_owner = requests.post(f'{BASE_URL}owners/', json={'name': 'Nick'})
response_get_owner = requests.get(f'{BASE_URL}owners/1')
response_post_ad = requests.post(f'{BASE_URL}advertisements/', json={'title': 'phone',
                                                                     'description': 'sell',
                                                                     'owner_id': 2})
response_get_ad = requests.get(f'{BASE_URL}advertisements/1')
response_patch_ad = requests.patch(f'{BASE_URL}advertisements/', json={'title': 'new_phone',
                                                                       'description': 'new_sell',
                                                                       'owner_id': 1})
response_delete_ad = requests.delete(f'{BASE_URL}advertisements/1')
