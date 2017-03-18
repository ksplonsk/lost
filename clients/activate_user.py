import requests
import sys
import json

args = dict()
args['username'] = sys.argv[2]
args['password'] = sys.argv[3]
args['role'] = sys.argv[4]

try:
    response = requests.post(
        url="{}rest/activate_user".format(sys.argv[1]),
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
        data={
            "arguments": json.dumps(args),
        },
    )
    print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
    print('Response HTTP Response Body: {content}'.format(content=response.content))
except requests.exceptions.RequestException:
    print('HTTP Request failed')


