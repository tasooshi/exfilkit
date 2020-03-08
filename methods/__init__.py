import argparse
import datetime
import email.utils
import functools
import random
import socket
import socketserver
import sys
import time

import lollipopz as lpz


class BaseHandler:

    BUFFER_LENGTH = 4096

    def init(self, args):
        self.args = args

    def execute(self):
        raise NotImplementedError

    def date_now_rfc_1123(self):
        now = datetime.datetime.utcnow()
        return email.utils.formatdate(now.timestamp(), False, True)

    def extra_args(self, parser):
        parser.add_argument('-lh', '--local-host', nargs='?', default='0.0.0.0')
        parser.add_argument('-lp', '--local-port', nargs='?', required=False, type=int)


class BaseServer(BaseHandler):

    def handle(self):
        raise NotImplementedError

    def output_write(self, content):
        if isinstance(content, str):
            content = content.encode('utf8')
        self.args['outfile'].write(content)
        self.args['outfile'].flush()

    def extra_args(self, parser):
        super().extra_args(parser)
        parser.add_argument('-o', '--outfile', type=argparse.FileType('wb'), default=sys.stdout)

    def execute(self):
        host = self.args['local_host']
        port = self.args['local_port']
        try:
            with self.SERVER_CLASS((host, port), functools.partial(DummyHandler, self)) as server:
                lpz.logger.info(f'Started service at {host}:{port}')
                server.serve_forever()
        except OSError as exc:
            lpz.logger.debug(exc.args[1])
            lpz.logger.info(f'Service could not be started at {host}:{port}')
        except KeyboardInterrupt:
            lpz.logger.info('Service stopped')


class DummyHandler(socketserver.BaseRequestHandler):

    def __init__(self, service, socket, client_address, tcpServer):
        self.service = service
        super().__init__(socket, client_address, tcpServer)

    def handle(self):
        self.service.handle(self.request, self.client_address)


class TCPServer(BaseServer):

    EOT_SEQUENCE = b'\n'
    SERVER_CLASS = socketserver.TCPServer

    def receive(self, request):
        data = b''
        if self.EOT_SEQUENCE:
            while not data.endswith(self.EOT_SEQUENCE):
                chunk = request.recv(self.BUFFER_LENGTH)
                if not chunk:
                    break
                data += chunk
            lpz.logger.debug(data)
        return data


class UDPServer(BaseServer):

    SERVER_CLASS = socketserver.UDPServer

    def receive(self, request):
        data = request[0]
        lpz.logger.debug(data)
        return data


class HTTPServer(TCPServer):

    EOT_SEQUENCE = b'\r\n\r\n'


class BaseClient(BaseHandler):

    RANDOM_DECOY = 4
    RANDOM_SLEEP = (1000, 10000)
    SOCKET_TYPE = None

    def send(self, body):
        incoming = b''
        if self.args['randomize']:
            time.sleep(random.randint(*self.RANDOM_SLEEP) / 1000.0)
        sock = socket.socket(socket.AF_INET, self.SOCKET_TYPE)
        if self.args['local_port']:
            try:
                sock.bind((self.args['local_host'], self.args['local_port']))
            except OSError as exc:
                lpz.logger.debug(exc.args[1])
                lpz.logger.info(f'Client could not be started!')
        try:
            remote_target = (self.args['remote_host'], self.args['remote_port'])
            sock.connect(remote_target)
        except ConnectionRefusedError:
            lpz.logger.info('Failed, connection refused!')
        else:
            sock.send(body)
            incoming = self.receive(sock)
            sock.close()
            lpz.logger.debug(incoming)
            lpz.logger.info(f'-> Payload delivered to {remote_target[0]}:{remote_target[1]}')
        return incoming

    def prepare_data(self, data):
        raise NotImplementedError

    def extra_args(self, parser):
        super().extra_args(parser)
        parser.add_argument('-i', '--infile', type=argparse.FileType('rb'), default=sys.stdin)
        parser.add_argument('-rh', '--remote-host', nargs='?', required=True)
        parser.add_argument('-rp', '--remote-port', nargs='?', required=True, type=int)
        parser.add_argument('-r', '--randomize', action='store_true')


class TCPClient(BaseClient):

    EOT_SEQUENCE = b'\n'
    SOCKET_TYPE = socket.SOCK_STREAM

    def receive(self, request):
        data = b''
        if self.EOT_SEQUENCE:
            while not data.endswith(self.EOT_SEQUENCE):
                chunk = request.recv(self.BUFFER_LENGTH)
                if not chunk:
                    break
                data += chunk
            lpz.logger.debug(data)
        return data


class UDPClient(BaseClient):

    SOCKET_TYPE = socket.SOCK_DGRAM

    def receive(self, sock):
        data = sock.recvfrom(self.BUFFER_LENGTH)
        lpz.logger.debug(data)
        return data
