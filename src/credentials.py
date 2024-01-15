#! /usr/bin/env python

from wsgiref.simple_server import make_server
import urllib
import json

# environ - словарь окружения http
# start_response - функция, для статуса ответа и заголовков
# QUERY_STRING - строка запроса
# REQUEST_METHOD - содержит HTTP-метод запроса (GET, POST, PUT, DELETE)
# оболочка zsh ~ % curl 'http://127.0.0.1:8888/?species=Time%20Lord'
# в URL ? - начало строки  %20 - пробел

names = {
    "Cyberman": "John Lumic",
    "Dalek": "Davros",
    "Judoon": "Shadow Proclamation Convention 15 Enforcer",
    "Human": "Leonardo da Vinci",
    "Ood": "Klineman Halpen",
    "Silence": "Tasha Lem",
    "Slitheen": "Coca-Cola salesman",
    "Sontaran": "General Staal",
    "Time Lord": "Rassilon",
    "Weeping Angel": "The Division Representative",
    "Zygon": "Broton"
}


def application(environ, start_response):
    if environ["REQUEST_METHOD"] == "GET":
        query_string = environ.get("QUERY_STRING", '')
        query_params = urllib.parse.parse_qs(query_string)

        species = query_params.get("species", [''])[0]

        if species in names:
            response_data = {"credentials": names[species]}
            status = "200 OK"
        else:
            response_data = {"credentials": "Unknown"}
            status = "404 Not Found"
    else:
        response_data = {"Error": "Method Not Allowed"}
        status = "405 Method Not Allowed"

    response_body = json.dumps(response_data).encode("utf-8")

    headers = [("Content-Type", "application/json")]
    start_response(status, headers)

    return [response_body]


def main():
    http = make_server(
        "localhost",
        8888,
        application,
    )

    http.serve_forever()


def test_get_time_lord_credentials():
    environ = {
        "REQUEST_METHOD": "GET",
        "QUERY_STRING": "species=Time%20Lord"
    }

    def start_response(status, headers):
        assert status == "200 OK"
        assert headers == [("Content-Type", "application/json")]

    response = application(environ, start_response)
    response_data = json.loads(b"".join(response).decode("utf-8"))
    assert response_data == {"credentials": "Rassilon"}


def test_get_unknown_species_credentials():
    environ = {
        "REQUEST_METHOD": "GET",
        "QUERY_STRING": "species=unknown"
    }

    def start_response(status, headers):
        assert status == "404 Not Found"
        assert headers == [("Content-Type", "application/json")]

    response = application(environ, start_response)
    response_data = json.loads(b"".join(response).decode("utf-8"))
    assert response_data == {"credentials": "Unknown"}


def test_method_not_allowed():
    environ = {
        "REQUEST_METHOD": "POST"
    }

    def start_response(status, headers):
        assert status == "405 Method Not Allowed"
        assert headers == [("Content-Type", "application/json")]

    response = application(environ, start_response)
    response_data = json.loads(b"".join(response).decode("utf-8"))
    assert response_data == {"Error": "Method Not Allowed"}


def tests():
    test_get_time_lord_credentials()
    test_get_unknown_species_credentials()
    test_method_not_allowed()


if __name__ == "__main__":
    try:
        tests()
        main()
    except KeyboardInterrupt:
        print("\nWeb-server was closed")
