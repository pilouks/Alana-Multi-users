import requests


_base = "http://localhost:5005/"

_status = _base + "status"
_parse = _base + "model/parse"


# Function to get a JSON from a localhost RASA server containing an evaluation of a parsed textual utterance
def parse_utterance(utterance):
    # Fill the request body
    payload = {"text": utterance}

    # Post the request
    response = requests.post(url=_parse, json=payload)

    # Fail if status code is not okay
    status_code = response.status_code
    if status_code != 200:
        raise Exception("Bad status code ({}) returned.".format(status_code))

    # Return the json
    data = response.json()
    return data


# Ensure local server is running and fail if not
def assert_server_health():
    # Attempt to communicate with the server
    try:
        response = requests.get(url=_base)
        status_code = response.status_code
    except:
        status_code = -1

    # Fail if no response
    if status_code != 200:
        raise ConnectionError("RASA server not found.")
