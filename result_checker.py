import re


class Etudiant(object):
    def __init__(self, name):
        self.name = name
        self.rank = 0
        self.eta_ranking = {}
        self.establishment = None

    def __repr__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return '"'+self.__repr__()+'"'


class Establishment(object):
    def __init__(self, name, capacity=0):
        self.name = name
        self.capacity = capacity
        self.students = []

    def __repr__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return '"'+self.__repr__()+'"'


def get_names(set_name, Obj_type):
    r_exp = re.compile(r'set '+set_name+' := "(?P<names>.*)"\s?;')
    names_list = re.match(r_exp, source.readline())
    while names_list is None:
        names_list = re.match(r_exp, source.readline())
    names_list = re.split(r'" "', names_list.groupdict().get('names'))
    return [Obj_type(name) for name in names_list]


def set_secondary_attr(param_name, attr_name, obj_list):
    r_exp = re.compile(r'param '+param_name+' :=\s+"(?P<obj_name>.*)"\s+(?P<attr>\d+)')
    new_attr = re.match(r_exp,  source.readline())
    while new_attr is None:
        new_attr = re.match(r_exp, source.readline())
    attr_list = [new_attr]
    r_exp = re.compile(r'\s+"(?P<obj_name>.*)"\s+(?P<attr>\d+)')
    new_attr = re.match(r_exp, source.readline())
    while new_attr is not None:
        attr_list.append(new_attr)
        new_attr = re.match(r_exp, source.readline())
    for o, a in zip(obj_list, attr_list):
        setattr(o, attr_name, int(a.groupdict().get('attr')))


with open('projet1.dat') as source:
    # Get students name list
    students = get_names('ETU', Etudiant)

    # Get establishment name list
    etas = get_names('ETA', Establishment)

    # Get establishments' capacities
    set_secondary_attr('capa', 'capacity', etas)

    # Get students' ranks
    set_secondary_attr('rank_etu', 'rank', students)

    # Get students' ranking by establishment
    while re.match(r'param rank_eta :', source.readline()) is None:
        pass
    reg = re.compile('\s+"(?P<stu_name>.*)"(?P<all_ranks>(?:\s+-?\d+)+)')
    for s in students:
        ranks = re.match(reg, source.readline())
        for r, eta in zip(ranks.groupdict().get('all_ranks').split(), etas):
            s.eta_ranking[eta] = int(r)


with open('projet1.out') as source:
    source.readline()
    source.readline()

    # Get students' allotment
    reg = re.compile(r'^\s+(.+)\n')
    for stu in students:
        source.readline()
        eta_name = re.sub(reg, r'\1', source.readline())
        stu.establishment = (e for e in etas if e.name == eta_name)

    source.readline()
    source.readline()
    source.readline()
    source.readline()

    # Get establishments' students
    reg = re.compile(r'^\t((?:[^\t\n]+\t?)*)\n')
    for eta in etas:
        source.readline()
        try:
            eta.students = list(map(lambda s_name: next(s for s in students if s.name == s_name),
                                re.findall(reg, source.readline())[0].split('\t')))
        except IndexError:
            pass
