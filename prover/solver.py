from .ast import *

queue = []


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
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.childs = []
        self.rule = []
        self.satis = []
        self.parent = parent
        self.chd_idx = -1

    def add_child(self, rule, node1=None, node2=None):
        assert node1
        if node2:
            self.childs.append((node1, node2))
        else:
            self.childs.append(node1)
        self.satis.append(0)
        self.rule.append(rule)

    def trace(self):
        if self.chd_idx == -1:
            print('{}: {}, by rule {} -> {}'.format(self.pos, queue[self.pos][0], 'P1 ', 'true'))
        else:
            imps = self.childs[self.chd_idx]
            binary = isinstance(imps, tuple)
            if binary:
                imps = (imps[0].pos, imps[1].pos)
            else:
                imps = imps.pos

            print('{}: {}, by rule {} -> {}'.format(self.pos, queue[self.pos][0], self.rule[self.chd_idx], imps))
            if binary:
                self.childs[self.chd_idx][0].trace()
                self.childs[self.chd_idx][1].trace()
            else:
                self.childs[self.chd_idx].trace()

    def update(self):
        if not self.parent:
            return True
        else:
            flag = False
            for i, item in enumerate(self.parent.childs):
                if isinstance(item, tuple):
                    if item[0] == self or item[1] == self:
                        self.parent.satis[i] += 1
                        if self.parent.satis[i] == 2:
                            self.parent.chd_idx = i
                            flag = True
                            break
                else:
                    if item == self:
                        self.parent.satis[i] += 1
                        self.parent.chd_idx = i
                        flag = True
                        break

            if flag:
                return self.parent.update()


def bfs_solver(seq):
    ret = False
    global queue
    root = Tree(0)
    queue.append((seq, root))
    head = 0

    while head < len(queue):
        now = queue[head][0]
        t = queue[head][1]
        if tautology(now):
            if t.update():
                ret = True
                break
        else:
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
                new_t = Tree(len(queue), parent=t)
                queue.append((Sequent(String(new_pre_list), String(new_post_list)), new_t))
                t.add_child('P2a', node1=new_t)

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
                new_t = Tree(len(queue), parent=t)
                queue.append((Sequent(String(new_pre_list), String(new_post_list)), new_t))
                t.add_child('P2b', node1=new_t)

            # Rule P3a
            for form in post_list:
                if isinstance(form, Formula):
                    if form.conn == Connective.AND:
                        new_post_list_1 = post_list[:]
                        new_post_list_2 = post_list[:]
                        new_post_list_1.remove(form)
                        new_post_list_2.remove(form)
                        new_post_list_1.append(form.get_op(0))
                        new_post_list_2.append(form.get_op(1))
                        new_t_1 = Tree(len(queue), parent=t)
                        queue.append((Sequent(now.pre, String(new_post_list_1)), new_t_1))
                        new_t_2 = Tree(len(queue), parent=t)
                        queue.append((Sequent(now.pre, String(new_post_list_2)), new_t_2))
                        t.add_child('P3a', node1=new_t_1, node2=new_t_2)

            # Rule P3b
            for form in pre_list:
                if isinstance(form, Formula):
                    if form.conn == Connective.AND:
                        new_pre_list = pre_list[:]
                        new_pre_list.remove(form)
                        new_pre_list.append(form.get_op(0))
                        new_pre_list.append(form.get_op(1))
                        new_t = Tree(len(queue), parent=t)
                        queue.append((Sequent(String(new_pre_list), now.post), new_t))
                        t.add_child('P3b', node1=new_t)

            # Rule P4a
            for form in post_list:
                if isinstance(form, Formula):
                    if form.conn == Connective.OR:
                        new_post_list = post_list[:]
                        new_post_list.remove(form)
                        new_post_list.append(form.get_op(0))
                        new_post_list.append(form.get_op(1))
                        new_t = Tree(len(queue), parent=t)
                        queue.append((Sequent(now.pre, String(new_post_list)), new_t))
                        t.add_child('P4a', node1=new_t)

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
                        new_t = Tree(len(queue), parent=t)
                        queue.append((Sequent(String(new_pre_list), String(new_post_list)), new_t))
                        t.add_child('P5a', node1=new_t)

            # Rule P5b
            # Rule P6a
            # Rule P6b

        head += 1

    """
    if hit != -1:
        ret = True
        history.append(('P1', queue[hit][0]))
        while queue[hit][-1] != -1:
            prev = queue[hit][-1]
            history.append((queue[hit][1], queue[prev][0]))
            hit = prev
    """

    if ret:
        root.trace()

    return ret
