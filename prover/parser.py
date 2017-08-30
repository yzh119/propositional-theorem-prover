from .ast import *

conn_dict = {'seq', 'and', 'or', 'imp', 'iff', 'neg'}


def remove_bracket(input_str):
    if input_str:
        cnt = 0
        flag = input_str[0] == '('
        for i, char in enumerate(input_str):
            if char == '(':
                cnt += 1
            elif char == ')':
                cnt -= 1
            if cnt == 0 and i != len(input_str) - 1:
                flag = False

        assert cnt == 0, "Unmatched bracket"
        if flag:
            return input_str[1:-1]
    return input_str


"""
def count_conn(input_str):
    cnt = 0
    input_str = input_str.replace(')', ' ')
    input_str = input_str.replace('(', ' ')
    input_str = input_str.replace(',', ' ')
    seq = input_str.split()

    for token in seq:
        if token in conn_dict:
            cnt += 1
    return cnt
"""


def parse_form(input_str):
    input_str = input_str.strip()
    input_str = remove_bracket(input_str)

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

    if k == -1:
        return Atom(input_str)

    conn_str = input_str[k:k + 3]
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

    str_l = input_str[0:k].strip()
    str_r = input_str[k + 3:].strip()

    str_l = remove_bracket(str_l)
    str_r = remove_bracket(str_r)

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
        str_r = chs[1].strip().strip('[').strip(']')
        ret = Sequent(parse_string(str_l, 'STR'), parse_string(str_r, 'STR'))
    elif level == 'STR':
        if len(input_str) == 0:
            return String([])
        chs = input_str.split(',')
        ret = String([parse_string(s, 'FOR') for s in chs])
    elif level == 'FOR':
        ret = parse_form(input_str)
    elif level == "ATOM":
        ret = Atom(input_str)
    else:
        raise Exception("Unexpected input.")
    return ret
