
from datetime import datetime


HTTP_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
HTTP_REASON = {
    200: "OK",
    404: "Not Found",
    405: "Method Not Allowed",
    415: "Unsupported Media Type",
}
PROTOCOLE = "HTTP/1.1"


class HttpRequest:
    def __init__(self, protocole, method, path, query, headers, body):
        self.protocole = protocole
        self.method = method
        self.path = path
        self.query = query
        self.headers = headers
        self.body = body

    @classmethod
    def from_message(cls, host, port, message):
        request = cls(
            protocole="HTTP/1.1",
            method="POST",
            path="/",
            query=None,  # TODO - NOT SUPPORTED
            headers={"Host": f"{host}:{port}"},
            body=message
        )
        return request

    @classmethod
    def parse(cls, raw_request):
        # split
        headers_block, body_block = raw_request.split(b"\n\n")
        headers = headers_block.split(b"\n")
        request_line = headers.pop(0)
        method, path, protocole = request_line.split(b" ")
        # process
        method = str(method, 'iso-8859-1')
        path = str(path, 'iso-8859-1')
        protocole = str(protocole, 'iso-8859-1')
        headers_dict = {}
        for raw_line in headers:
            line = str(raw_line, 'iso-8859-1')
            key, value = line.split(": ", 1)
            headers_dict[key] = value
        body = body_block.decode("utf-8")
        # return object
        request = cls(
            protocole=protocole,
            method=method,
            path=path,
            query=(),  # TODO - NOT SUPPORTED
            headers=headers_dict,
            body=body,
        )
        return request

    def assemble(self):
        protocole = self.protocole.upper()
        method = self.method.upper()
        path = str(self.path)
        headers = dict(self.headers)
        content = self.body.encode("utf-8")
        content_length = len(content)
        headers.update({
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Length": content_length,
            "User-Agent": "Smiglo Ultra-Photo-Client!",
        })
        request_line = f"{method} {path} {protocole}\n".encode(
            "latin-1", "strict")
        header_lines = [f"{key}: {value}" for key, value in headers.items()]
        header_block = "\n".join(header_lines).encode("latin-1", "strict")

        request = request_line + header_block + b"\n\n" + content
        return request


class HttpResponse:
    def __init__(self, protocole, code, reason, headers, body):
        self.protocole = protocole
        self.code = code
        self.reason = reason
        self.headers = headers
        self.body = body

    @classmethod
    def from_code(cls, code, body):
        response = cls(
            protocole=PROTOCOLE,
            code=code,
            reason=HTTP_REASON[code],
            headers={},
            body=body,
        )
        return response

    @classmethod
    def parse(cls, raw_response):
        # split response
        headers_block, body_block = raw_response.split(b"\n\n")
        headers = headers_block.split(b"\n")
        status_line = headers.pop(0)
        protocole, code, reason = status_line.split(b" ", 2)
        # preprocess response
        protocole = str(protocole, 'iso-8859-1')
        code = int(str(code, 'iso-8859-1'))
        reason = str(reason, 'iso-8859-1')
        headers_dict = {}
        for raw_line in headers:
            line = str(raw_line, 'iso-8859-1')
            key, value = line.split(": ", 1)
            headers_dict[key] = value
        body = body_block.decode("utf-8")
        # return object
        response = cls(
            protocole=protocole,
            code=code,
            reason=reason,
            headers=headers_dict,
            body=body,
        )
        return response

    def assemble(self):
        # get data
        protocole = self.protocole
        code = self.code
        reason = self.reason
        headers = self.headers
        body = self.body

        # preprocess data
        if not isinstance(body, str):
            body = str(body)
            print("Server has been asked to respond with an object.")
        encoding = "utf-8"
        content = body.encode(encoding)
        content_length = len(content)
        date_str = datetime.utcnow().strftime(HTTP_DATETIME_FORMAT)
        if 200 <= code < 300:
            connection_command = "keep-alive"
        else:
            connection_command = "close"

        # add headers
        headers.update({
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Length": content_length,
            "Date": date_str,
            "Connection": connection_command,
            "Server": "Smiglo Modern Photo-Server!",
        })

        # assembly bytes response
        status_line = f"{protocole} {code} {reason}\n".encode(encoding)
        headers_block = "\n".join([
            f"{key}: {value}" for key, value in headers.items()])
        headers_block = headers_block.encode("latin-1", "strict")
        raw_response = status_line + headers_block + b"\n\n" + content
        return raw_response
