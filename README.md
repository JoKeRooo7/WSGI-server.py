## wsgi

My server is written using the 'wsgiref` library. Presented in the file `credentials.py `

Learn more about the server - [wiki](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface ).


## Launch

The server itself is started using a script `credentials.py `.


### `main()`

The function `main()` - creates an application server at the address `localhost`, on port `8888`, application - creates an application. `http.serve_forever()` - starts the web server and starts an endless request processing cycle.


### `application(environ, start_response)`

The `application(environment, start_response)` function is called by the web server. It handles all requests. Checks requests for availability, only `GET` requests have been processed.
If the request is `GET`, it receives a string from environ and checks it with a pre-prepared database `names` and returns its value, depending on the submitted key.

There are also tests.
