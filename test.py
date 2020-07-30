# Just calls all APIs once to check if its working
import requests


def test(method, url, payload={}, headers={}):
    try:
        response = requests.request(method, url, headers=headers, data=payload)
    except Exception as e:
        print("\n\n\n\n\n\n\n")
        print("GET failed with " + str(e))
        print("\n\n\n\n\n\n\n")
    print(method + " response: " + response.text)


if __name__ == '__main__':
    test("GET", "http://ee9f283d3026.ngrok.io")
    test("POST", "http://ee9f283d3026.ngrok.io", "{\n    \"test\": \"value\"\n}", {'Content-Type': 'application/json'})
