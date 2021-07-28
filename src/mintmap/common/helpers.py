# helpers.py

import gzip
import io
import itertools


def open_file(path):
    input_file = None

    if path.endswith('.gz') or path.endswith('.gzip'):
        input_file = io.BufferedReader(gzip.open(path, 'rb'))
    else:
        input_file = open(path, 'rb')

    return map(
        lambda line: line.decode(encoding='UTF-8',
                                 errors='strict').strip(),
        input_file.readlines()
    )


def slice(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def tr(iterable):
    tds = "".join(map(lambda i: f"<th>{str(i)}</th>", iterable))
    return f"<tr>{tds}</tr>"


def csv(iterable):
    return ",".join(map(lambda i: str(i), iterable))


def csv_html(iterable):
    return ",<br>".join(map(lambda i: str(i), iterable))


def tsv(iterable):
    return "\t".join(map(lambda i: str(i), iterable))


def tds(iterable):
    return ' '.join(map(lambda i: "<td>{i}</td>", iterable))


def reverse_complement(sequence):
    intab = "ATCG"
    outtab = "TAGC"
    translation = sequence.maketrans(intab, outtab)
    complement = sequence.translate(translation)
    reverse_complement = complement[::-1]
    return reverse_complement
