from .ast import *


def parse_form(input_str):
    input_str = input_str.strip()
    cnt = 0
    space = 0
    k = -1

    if input_str.startswith('neg'):
        k = 0
    else:
        for i, char in enumerate(input_str):
            if char == '(':
                cnt += 1
            elif char == ')':
                cnt -= 1
            elif char != ' ':
                if cnt == 0 and space > 0:
                    k = i
                    break
            else:
                space += 1

    assert k > -1, "Invalid Formula"

    conn_str = input_str[k:k+3]
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

    str_l = input_str[0:k].strip().strip('(').strip(')')
    str_r = input_str[k+3:].strip().strip('(').strip(')')
    detect_l = ' ' in str_l
    detect_r = ' ' in str_r
    return Formula(conn,
                   parse_string(str_l, 'FOR' if detect_l else 'ATOM'),
                   parse_string(str_r, 'FOR' if detect_r else 'ATOM'))


def parse_string(input_str, level):
    ret = None
    level = level.strip()
    if level == 'SEQ':
        chs = input_str.split('seq')
        assert len(chs) == 2, "Unexpected input"
        str_l = chs[0].strip().strip('[').strip(']')
        str_r = chs[0].strip().strip('[').strip(']')
        ret = Sequent(parse_string(str_l, 'STR'), parse_string(str_r, 'STR'))
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
