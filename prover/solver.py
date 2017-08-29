from .ast import *


def tautology(seq):
    assert isinstance(seq, Sequent)
    if not seq.post.forms:
        return True
    atom_l_arr = []
    atom_r_arr = []
    for form in seq.pre.forms:
        if isinstance(form, Atom):
            atom_l_arr.append(form)

    for form in seq.post.forms:
        if isinstance(form, Atom):
            atom_r_arr.append(form)

    if set(atom_l_arr) & set(atom_r_arr):
        return True
    return False


class Tree(object):
    def __init__(self):
        pass


def bfs_solver(seq):
    history = []
    ret = False
    queue = [(seq, None, -1)]  # tuple: (seq, approach, prev, )
    head = 0
    tail = 1
    hit = -1
    while head < tail:
        now = queue[head][0]
        if tautology(now):
            hit = head
            break
        head += 1
        '''
        # Rule P2a
        queue.append((new_seq, 'Rule P2a', now))
        # Rule P2b
        queue.append((new_seq, 'Rule P2b', now))
        # Rule P3a
        queue.append((new_seq, 'Rule P3a', now))
        # Rule P3b
        queue.append((new_seq, 'Rule P3b', now))
        # Rule P4a
        queue.append((new_seq, 'Rule P4a', now))
        # Rule P4b
        queue.append((new_seq, 'Rule P4b', now))
        # Rule P5a
        queue.append((new_seq, 'Rule P5a', now))
        # Rule P5b
        queue.append((new_seq, 'Rule P5b', now))
        # Rule P6a
        queue.append((new_seq, 'Rule P6a', now))
        # Rule P6b
        queue.append((new_seq, 'Rule P6b', now))
        '''

    if hit != -1:
        ret = True
        history.append(('P1', queue[hit][0]))
        while queue[hit][-1] != -1:
            prev = queue[hit][-1]
            history.append((queue[hit][1], queue[prev][0]))
            hit = prev

    return ret, history
