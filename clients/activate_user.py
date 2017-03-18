import requests


def send_request():
    # add_user
    # POST http://127.0.0.1:8080/rest/add_user

    try:
        response = requests.post(
            url="http://127.0.0.1:8080/rest/add_user",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            },
            data={
                "arguments": "{\"username\":\"ksplonsk\",\"password\":\"chester\",\"role\":\"Logistics Officer\"}",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


        