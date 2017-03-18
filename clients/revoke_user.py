import requests
import sys

try:
    response = requests.post(
        url="http://127.0.0.1:8080/rest/revoke_user",
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
        data={
            "arguments": "{'username':'river'}",
        },
    )
    print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
    print('Response HTTP Response Body: {content}'.format(content=response.content))
except requests.exceptions.RequestException:
    print('HTTP Request failed')

