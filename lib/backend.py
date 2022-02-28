
from lib.client import HttpClient
from lib.common import HttpRequest, HttpResponse
from lib.server import HttpServer


class Backend:
    def __init__(self, config):
        listener_port = config["listener_port"]
        self.listener_port = listener_port
        self.handle_in_message = None
        self.foreign_host = None

    def register_handle_callback(self, handle_callback):
        self.handle_in_message = handle_callback

    def start(self):
        self.server = HttpServer(self.listener_port, self._handle_request)
        self.client = HttpClient()
        # TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO
        self.client.backend_ref = self
        self.foreign_host = None # wait for connection from foreign host

    def stop(self):
        self.server.stop()
        self.client.stop()

    def send_out_message(self, out_message):
        # prepare request
        request = HttpRequest.from_message(
            host=self.foreign_host,
            port=self.listener_port,
            message=out_message,
        )

        # send request
        response = self.client.send(
            self.foreign_host, self.listener_port, request)

        # read response
        if response.code != 200:
            raise ConnectionError(
                f"Server responded with error: {response.code},"
                f" {response.reason}, {response.body}")
        response_content = response.body
        return response_content

    def _handle_request(self, request: HttpRequest) -> HttpResponse:
        # handle wrong method
        if request.method != "POST":
            return HttpResponse.from_code(
                code=405, body=f"Wrong HTTP request method: {request.method}")

        # handle wrong resource path
        if request.path != "/":
            return HttpResponse.from_code(
                code=404, body=f"Cannot find resource: {request.path}")

        # handle wrong content type
        content_type = request.headers.get("Content-Type")
        if content_type != "text/plain; charset=utf-8":
            return HttpResponse.from_code(
                code=415,
                body=f"Wrong HTTP request content type: {content_type}"
            )

        # everything OK
        in_message = request.body
        response_content = self.handle_in_message(in_message)
        return HttpResponse.from_code(code=200, body=response_content)
