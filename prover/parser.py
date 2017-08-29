from .ast import *


def parse_form(input_str):
    cnt = 0
    k = -1
    for i, char in enumerate(input_str):
        if char == '(':
            cnt += 1
        elif char == ')':
            cnt -= 1
        elif char != ' ':
            if cnt == 0:
                k = i
                break
    assert k > -1, "Invalid Formula"

    conn_str = input_str[k, k + 3]
    conn = None
    if conn_str == 'neg':
        conn = Connective.NEG

    if conn_str == 'and':
        conn = Connective.AND

    if conn_str == 'or ':
        conn = Connective.OR

    if conn_str == 'imp':
        conn = Connective.IMP

    if conn_str == 'iff':
        conn = Connective.IFF

    assert conn, "Invalid Formula"

    l_str = input_str[0:k].strip().strip('(').strip(')')
    r_str = input_str[k+3:-1].strip().strip('(').strip(')')
    return Formula(conn, parse_string(l_str, 'FOR'), parse_string(r_str, 'FOR'))


def parse_string(input_str, level):
    ret = None
    level = level.strip()
    if level == 'SEQ':
        chs = input_str.split('seq')
        assert len(chs) == 2, "Unexpected input"
        ret = Sequent(parse_string(chs[0], 'STR'), parse_string(chs[1], 'STR'))
    elif level == 'STR':
        if len(input_str) == 0:
            return Empty
        chs = input_str.split(',')
        ret = String([parse_string(s, 'FOR') for s in chs])
    elif level == 'FOR':
        ret = parse_form(input_str)
    elif level == "ATOM":
        ret = Atom(input_str)
    else:
        raise Exception("Unexpected input.")
    return ret
