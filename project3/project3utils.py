import numpy as np
from urllib.parse import urlparse
from collections import Counter
from scipy.stats import entropy

from cc2ld import second_level_domains_by_country_code as sld_by_cc

alphabet = 'abcdefghijklmnopqrstuvwxyz'
vowels = 'aeiou'
consonants = [char for char in alphabet if char not in vowels]
digits = '0123456789'
other_chars = '.-/:_@'
all_chars = alphabet + digits + other_chars
char_label_map = {
    '.': 'dot',
    '-': 'hyphen',
    '/': 'slash',
    ':': 'colon',
    '_': 'underscore',
    '@': 'at'
}
def get_char_count_label(char):
    return 'char_' + char_label_map.get(char, char)

def get_char_counts(string, key_prefix=''):
    counter = Counter(string)
    counts = {(key_prefix + get_char_count_label(c)): counter[c] for c in all_chars}
    counts[key_prefix + 'vowels'] = sum(counter[c] for c in vowels)
    counts[key_prefix + 'consonants'] = sum(counter[c] for c in consonants)
    counts[key_prefix + 'digits'] = sum(counter[c] for c in digits)
    total_chars = len(string)
    counts[key_prefix + 'total_chars'] = total_chars
    counts[key_prefix + 'empty_string'] = int(total_chars == 0)
    counts[key_prefix + 'entropy'] = entropy(list(counter.values()))
    return counts

def get_features_from_url(url):
    url = url.lower()
    url = urlparse(url)
    full_domain = url.netloc
    chunks = full_domain.split('.')
    try:
        for chunk in chunks:
            int(chunk)
        is_raw_ip = 1
        domain_start_index = 0
    except:
        is_raw_ip = 0
        domain_start_index = -1 * min(2, len(chunks))
        if domain_start_index == -2 and chunks[-2] in sld_by_cc[chunks[-1]]:
            domain_start_index = -3
    domain = '.'.join(chunks[domain_start_index:])
    subdomain = '.'.join(chunks[:domain_start_index])
    path = url.path
    if path and path[0] == '/': path = path[1:]
    if path and path[-1] == '/': path = path[:-1]
    features = get_char_counts(domain, 'domain_')
    features.update(get_char_counts(subdomain, 'subdomain_'))
    features.update(get_char_counts(path, 'path_'))
    features.update({
        'full_domain': full_domain,
        'domain': domain,
        'subdomain': subdomain,
        'path': path,
        'domain_is_dot_com': int(chunks[-1] == 'com'),
        'subdomain_is_www': int(subdomain == 'www'),
        'path_ends_in_php': int(path[-4:] == '.php'),
        'https': int(url.scheme == 'https'),
        'domain_is_raw_ip': is_raw_ip
    })
    return features

assert get_features_from_url('http://www.foo.co.uk')['domain'] == 'foo.co.uk'
assert get_features_from_url('http://www.foo.com')['domain'] == 'foo.com'

numeric_feature_columns = []
nonpath_feature_columns = []
path_feature_columns = []
for key, val in get_features_from_url('http://www.blah.com/foo').items():
    if type(val) != str:
        numeric_feature_columns.append(key)
        if key[0:4] == 'path':
            path_feature_columns.append(key)
        else:
            nonpath_feature_columns.append(key)
