__author__ = 'Piotr Moczurad and Michal Ciolczyk'

import os
import sys
import re
import codecs

re_flags = re.MULTILINE | re.U

author_pattern = re.compile(r'<META NAME="AUTOR" CONTENT="(.+)">', re_flags)
dept_pattern = re.compile(r'<META NAME="DZIAL" CONTENT="(.+)">', re_flags)
key_pattern = re.compile(r'<META NAME="KLUCZOWE_?\d*" CONTENT="(.+)">', re_flags)
text_pattern = re.compile(r'<P>(.+)<META NAME="AUTOR"', re_flags | re.DOTALL)
phrase_pattern = re.compile(r'([\w \-+*:,;\.]+)([\.?!]+|$)', re_flags)
abbrev_pattern = re.compile(r'\s\w{1,4}\.', re_flags)
#lepiej widac na debuggex.com
num_pattern = re.compile(
    r'-32768|[-\s](3276[0-7]|327[0-5]\d|327[0-5]\d{2}|32[0-6]\d{3}|3[0-1]\d{4}|[1-2]?\d{1,4})(([.,;:]\s)|\s)', re_flags)
float_pattern = re.compile(r'(-?(\d+\.\d*|\.\d+)(?:(e|E)\-?\d+)?)[.,;:]?\s', re_flags)
#ponizsze regexy czytelne tylko na debuggexie
dates_pattern = re.compile(
    r'(?P<yearA>\d{4})(?P<separatorA>[-\./])((?P<monthA1>0[13578]|1[02])'
    r'(?P=separatorA)(?P<dayA1>[0-2]\d|3[0-1])|((?P<monthA2>0[469]|11)'
    r'(?P=separatorA)(?P<dayA2>[0-2]\d|30))|((?P<monthA3>02)(?P=separatorA)'
    r'(?P<dayA3>[0-1]\d|2[0-9])))|((?P<dayB1>[0-2]\d|3[0-1])'
    r'(?P<separatorB1>[-\./])(?P<monthB1>0[13578]|1[02])|(?P<dayB2>[0-2]\d|30)'
    r'(?P<separatorB2>[-\./])(?P<monthB2>0[469]|11)|(?P<dayB3>[0-1]\d|2[0-9])'
    r'(?P<separatorB3>[-\./])(?P<monthB3>02))((?P=separatorB1)|(?P=separatorB2)|(?P=separatorB3))'
    r'(?P<yearB>\d{4})',
    re_flags)  # TODO: Fix accepting 00 as day
emails_pattern = re.compile(
    r'([A-Za-z0-9+\-]([A-Za-z0-9+\-]|[A-Za-z0-9+\-\.][A-Za-z0-9+\-])+'
    r'@[A-Za-z0-9]([A-Za-z\.0-9][A-Za-z0-9]|[A-Za-z0-9])*\.[A-Za-z0-9]{2,4})',
    re_flags)
# uwzglednione zostalo takze to, ze adres e-mail musi konczyc sie TLD


def my_match(pattern, content):
    match = pattern.search(content)
    if match:
        return match.groups()[0]
    else:
        return ""


def multi_match(pattern, content):
    matches = re.findall(pattern, content)
    return ", ".join(matches)


def count_matches(pattern, content):
    match = pattern.findall(content)
    if match:
        return len(match)
    else:
        return 0


def count_different_matches(pattern, content):
    match = pattern.findall(content)
    if match:
        s = set()
        for x in match:
            s.add(x)
        return len(s)
    else:
        return 0


def count_different_dates(content):
    matches = dates_pattern.finditer(content)
    if matches:
        s = set()
        for match in matches:
            day = ""
            month = ""
            year = ""
            groups = match.groupdict()
            for g in groups:
                v = groups[g]
                if g[0:3] == "day" and v is not None:
                    day = v
                elif g[0:5] == "month" and v is not None:
                    month = v
                elif g[0:4] == "year" and v is not None:
                    year = v
            s.add(year + "-" + month + "-" + day)
        return len(s)
    else:
        return 0


def count_ints(content):
    ints = map(lambda m: m[0] if isinstance(m, tuple) else m,
               num_pattern.findall(content))
    return len(set(ints))


def process_file(file_path):
    fp = codecs.open(file_path, 'rU', 'iso-8859-2')

    content = fp.read()

    #
    #  INSERT YOUR CODE HERE
    #

    fp.close()
    print("nazwa pliku: " + file_path)
    print("autor: " + my_match(author_pattern, content))
    print("dzial: " + my_match(dept_pattern, content))
    print("slowa kluczowe: " + multi_match(key_pattern, content))
    text = my_match(text_pattern, content)
    print("liczba zdan: " + str(count_matches(phrase_pattern, text)))
    print("liczba skrotow: " + str(count_different_matches(abbrev_pattern, text)))
    print("liczba liczb calkowitych z zakresu int: " + str(count_ints(text)))
    print("liczba liczb zmiennoprzecinkowych: " + str(count_different_matches(float_pattern, text)))
    print("liczba dat: " + str(count_different_dates(text)))
    print("liczba adresow email: " + str(count_different_matches(emails_pattern, text)))
    print("\n")


try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)

tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            process_file(filepath)