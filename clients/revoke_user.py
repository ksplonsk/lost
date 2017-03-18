import requests
import sys

try:
    response = requests.post(
        url="{}rest/revoke_user".format(sys.argv[1]),
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
        data={
            "arguments": "{\"username\":{}}".format(sys.argv[2]),
        },
    )
    print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
    print('Response HTTP Response Body: {content}'.format(content=response.content))
except requests.exceptions.RequestException:
    print('HTTP Request failed')

