__VERSION__ = '0.1'

import argparse
import logging
import socket

import whois
import selenium.webdriver

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

_alt_rules = [
    ('m', 'rn'),
    ('l', 'I'),
    ('l', '1'),
    ('d', 'cl'),
    ('i', 'j'),
    ('w', 'vv'),
    ('y', 'v')
]


def load_alteration_rules(path):
    """Load alteration rules from path

    :param path: File path string
    """
    alt_rules = []
    with open(path) as file:
        for line in file:
            parts = line.split(' ')
            if len(parts) >= 2:
                alt_rules.append((parts[0].strip(), parts[1].strip()))
    global _alt_rules
    _alt_rules = tuple(alt_rules)


def get_alterations(domain, alter_tld=True, max_pct_length=0.1):
    """Create a permutation of all alterations of the given domain

    :param domain: The domain to alter
    """
    #: set of (src string, last modification position)
    open = set(((domain, -1),))
    closed = set()

    while len(open) > 0:
        d, i = open.pop()
        closed.add(d)

        i += 1
        if i >= len(d):
            # i is off right end.  No alterations are possible.
            continue

        if float(len(d) - len(domain)) / len(domain) > max_pct_length:
            # The string is too long.  Skip.
            continue

        # Run all alterations of d
        for src, dest in _alt_rules:
            pos = d[i:].find(src)
            if pos == -1:
                open.add((d, i))
            else:
                new = d[:i+pos] + dest + d[i+pos+len(src):]
                open.add((new, i+pos))

    closed.remove(domain)
    return closed

AVAILABLE = 0
REGISTERED = 1
UNKNOWN_TLD = 2
def is_registered(domain):
    try:
        whoisinfo = whois.query(domain)
        if whoisinfo is None:
            return AVAILABLE
    except Exception as e:
        if str(e).startswith("Unknown TLD"):
            logger.debug("Unknown TLD: {}".format(domain))
            return UNKNOWN_TLD
    return REGISTERED


def get_screenshot(driver, domain):
    """Get screenshots of the domain and save them to http.{domain}.png and https.{domain}.png

    :param driver: Webdriver (Selenium, etc)
    :param domain: Domain to visit
    """
    http_path = 'http.'+domain+'.png'
    driver.get('http://' + domain)
    driver.save_screenshot(http_path)
    https_path = 'https.'+domain+'.png'
    driver.get('https://' + domain)
    driver.save_screenshot(https_path)
    print("{0} screenshots are saved as...\n{1}\n{2}".format(domain, http_path, https_path))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--alt", required=False, type=str, help="Path to alteration text file.  Each line represents a source string followed by a space and then the replacement string.")
    parser.add_argument("-d", "--debug", required=False, const=True, default=False, action="store_const", help="Show debug information")
    parser.add_argument("-s", "--screenshot", required=False, const=True, default=False, action="store_const", help="Capture screenshot of altered domains")
    parser.add_argument("-l", "--max_pct_length", required=False, type=float, default=0.1, help="Maximum percent increase in length over the starting domain.  Default=0.1")
    parser.add_argument("site", type=str, help="Domain name to test")
    args = parser.parse_args()

    if args.alt is not None:
        load_alteration_rules(args.alt)

    if args.debug:
        logger.setLevel(level=logging.DEBUG)

    test_domains = get_alterations(args.site, max_pct_length=args.max_pct_length)
    logger.debug("{0} is altered to {1}".format(args.site, test_domains))

    driver = None
    if args.screenshot:
        driver = selenium.webdriver.Chrome('chromedriver')

    for domain in test_domains:
        reg = is_registered(domain)
        if reg == AVAILABLE:
            print("Available: {}".format(domain))
            continue
        elif reg == UNKNOWN_TLD:
            continue
        else:
            try:
                socket.gethostbyname(domain)
            except socket.gaierror:
                print("Registered, but no IP address: {}".format(domain))
                continue

            if driver is not None:
                logger.debug("Getting screenshot for {}".format(domain))
                get_screenshot(driver, domain)

    if driver is not None:
        driver.quit()

if __name__ == "__main__":
    main()

