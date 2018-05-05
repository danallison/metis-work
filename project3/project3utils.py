from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
from collections import Counter

from cc2ld import second_level_domains_by_country_code as sld_by_cc

# secrets.py contains credentials, etc.
import secrets

def with_remote_sql_session(function):
    # Hat tip: https://stackoverflow.com/a/38001815
    with SSHTunnelForwarder(
            (secrets.server_ip_address, 22),
            ssh_username=secrets.ssh_username,
            ssh_pkey=secrets.ssh_private_key_path,
            ssh_private_key_password=secrets.ssh_private_key_password,
            remote_bind_address=('127.0.0.1', 5433)
        ) as tunnel:

        tunnel.start()

        engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{db}'.format(
            user=secrets.pg_user,
            password=secrets.pg_password,
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            db=secrets.pg_user
        ))

        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            return function(session)
        finally:
            session.close()

alphabet = 'abcdefghijklmnopqrstuvwxyz'
vowels = 'aeiou'
consonants = [char for char in alphabet if char not in vowels]
digits = '0123456789'
other_chars = '.-'
all_chars = alphabet + digits + other_chars
char_label_map = {
    '.': 'dot',
    '-': 'hyphen'
}
def get_char_count_label(char):
    return 'char_' + char_label_map.get(char, char)

def get_domain_char_counts(string, key_prefix=''):
    counter = Counter(string)
    counts = {(key_prefix + get_char_count_label(c)): counter[c] for c in all_chars}
    counts[key_prefix + 'vowels'] = sum(counter[c] for c in vowels)
    counts[key_prefix + 'consonants'] = sum(counter[c] for c in consonants)
    counts[key_prefix + 'digits'] = sum(counter[c] for c in digits)
    counts[key_prefix + 'total_chars'] = len(string)
    return counts

def get_features_from_url(url):
    url = url.lower()
    if url[0:7] not in ('http://', 'https:/'):
        url = 'http://' + url
    url = urlparse(url)
    full_domain = url.netloc
    chunks = full_domain.split('.')
    domain_start_index = -2
    if chunks[-2] in sld_by_cc[chunks[-1]]:
        domain_start_index -= 1
    domain = '.'.join(chunks[domain_start_index:])
    subdomain = '.'.join(chunks[:domain_start_index])
    features = get_domain_char_counts(domain, 'domain_')
    features.update(get_domain_char_counts(subdomain, 'subdomain_'))
    features.update({
        'full_domain': full_domain,
        'domain': domain,
        'subdomain': subdomain
    })
    return features

assert get_features_from_url('http://www.foo.co.uk')['domain'] == 'foo.co.uk'
assert get_features_from_url('http://www.foo.com')['domain'] == 'foo.com'
