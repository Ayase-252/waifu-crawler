import requests_mock
import requests


def async_request(url):
    while True:
        url = yield requests.get(url)


@requests_mock.Mocker()
def main(mocker):
    mocker.get('mock://abc.de')
    async_request_iter = async_request('mock://abc.de')
    resp = next(async_request_iter)
    print(resp)

main()
