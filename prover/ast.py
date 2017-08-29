from enum import Enum, unique


@unique
class Connective(Enum):
    NEG = 0,
    AND = 1,
    OR = 2,
    IMP = 3,
    IFF = 4


class Atom(object):
    def __init__(self, name=None):
        self._name = name

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


Empty = Atom()


class Formula(object):
    def __init__(self, conn, op_l=None, op_r=None):
        super(Formula, self).__init__()
        self._conn = conn
        self._op_l = op_l
        self._op_r = op_r

    @property
    def conn(self):
        return self._conn

    def get_op(self, idx):
        if idx == 0:
            return self._op_l
        else:
            return self._op_r

    def __str__(self):
        if self._conn == Connective.AND:
            return '(' + str(self._op_l) + ' and ' + str(self._op_r) + ')'
        if self._conn == Connective.OR:
            return '(' + str(self._op_l) + ' or ' + str(self._op_r) + ')'
        if self._conn == Connective.IMP:
            return '(' + str(self._op_r) + ' imp ' + str(self._op_r) + ')'
        if self._conn == Connective.IFF:
            return '(' + str(self._op_l) + ' iff ' + str(self._op_r) + ')'
        if self._conn == Connective.NEG:
            return '(' + 'neg ' + str(self._op_r) + ')'


class String(object):
    def __init__(self, forms):
        super(String, self).__init__()
        self._forms = forms

    @property
    def forms(self):
        return self._forms

    def __str__(self):
        return '[' + ', '.join([str(form) for form in self._forms]) + ']'


class Sequent(object):
    def __init__(self, pre, post):
        super(Sequent, self).__init__()
        self._pre = pre
        self._post = post

    @property
    def pre(self):
        return self._pre

    @property
    def post(self):
        return self._post

    def __str__(self):
        return str(self._pre) + ' seq ' + str(self._post)
