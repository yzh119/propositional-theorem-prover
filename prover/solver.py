from .ast import *


def tautology(seq):
    assert isinstance(seq, Sequent)
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
    queue = [(seq, None, -1)]  # tuple: (seq, approach, prev)
    head = 0
    hit = -1
    while head < len(queue):
        now = queue[head][0]
        if tautology(now):
            hit = head
            break

        # Rule P2a
        pre_list = now.pre.forms
        post_list = now.post.forms
        for form in post_list:
            new_pre_list = pre_list[:]
            new_post_list = post_list[:]
            new_post_list.remove(form)
            new_term = Formula(Connective.NEG, op_l=Atom(''), op_r=form)
            if isinstance(form, Formula):
                if form.conn == Connective.NEG:
                    new_term = form.get_op(1)
            new_pre_list.append(new_term)
            queue.append((Sequent(String(new_pre_list), String(new_post_list)), 'P2a', head))

        # Rule P2b
        for form in pre_list:
            new_pre_list = pre_list[:]
            new_pre_list.remove(form)
            new_post_list = post_list[:]
            new_term = Formula(Connective.NEG, op_l=Atom(''), op_r=form)
            if isinstance(form, Formula):
                if form.conn == Connective.NEG:
                    new_term = form.get_op(1)
            new_post_list.append(new_term)
            queue.append((Sequent(String(new_pre_list), String(new_post_list)), 'P2b', head))

        # Rule P3a
        # Rule P3b
        for form in pre_list:
            if isinstance(form, Formula):
                if form.conn == Connective.AND:
                    new_pre_list = pre_list[:]
                    new_pre_list.remove(form)
                    new_pre_list.append(form.get_op(0))
                    new_pre_list.append(form.get_op(1))
                    queue.append((Sequent(String(new_pre_list), now.post), 'P3b', head))

        # Rule P4a
        for form in post_list:
            if isinstance(form, Formula):
                if form.conn == Connective.OR:
                    new_post_list = post_list[:]
                    new_post_list.remove(form)
                    new_post_list.append(form.get_op(0))
                    new_post_list.append(form.get_op(1))
                    queue.append((Sequent(now.pre, String(new_post_list)), 'P4a', head))

        # Rule P4b
        # Rule P5a
        for form in post_list:
            if isinstance(form, Formula):
                if form.conn == Connective.IMP:
                    new_pre_list = pre_list[:]
                    new_post_list = post_list[:]
                    new_post_list.remove(form)
                    new_pre_list.append(form.get_op(0))
                    new_post_list.append(form.get_op(1))
                    queue.append((Sequent(String(new_pre_list), String(new_post_list)), 'P5a', head))

        # Rule P5b
        # Rule P6a
        # Rule P6b
        head += 1

    if hit != -1:
        ret = True
        history.append(('P1', queue[hit][0]))
        while queue[hit][-1] != -1:
            prev = queue[hit][-1]
            history.append((queue[hit][1], queue[prev][0]))
            hit = prev

    return ret, history
