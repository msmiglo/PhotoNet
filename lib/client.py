
from lib.common import HttpRequest, HttpResponse


class HttpClient:
    def __init__(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def send(self, host, port, request):
        # =====================
        # === short circuit ===
        # =====================
        from time import sleep
        sleep(0.28)
        dummy = request.body
        request.body = dummy[::-1]

        request = HttpRequest.parse(request.assemble())

        response = self.backend_ref._handle_request(request)
        return response
        # =====================

        if not isinstance(request, HttpRequest):
            raise TypeError("Please pass `HttpRequest` object.")
        raw_request = request.assemble()
        self.socket.write(host, port, raw_request)
        raw_response = self.socket.read(host, port, timeout=TIMEOUT)
        response = HttpResponse.parse(raw_response)
        return response
