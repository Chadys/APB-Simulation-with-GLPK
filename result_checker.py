import re


class Etudiant(object):
    def __init__(self, name):
        self.name = name
        self.eta_ranking = []
        self.rank = 0

    def __repr__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return '"'+self.__repr__()+'"'


class Establishment(object):
    def __init__(self, name, capacity=0):
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return '"'+self.__repr__()+'"'

def get_names(set_name, Obj_type):
    names_list = re.match(r'set '+set_name+' := "(?P<names>.*)";', source.readline())
    while names_list is None:
        names_list = re.match(r'set ' + set_name + ' := "(?P<names>.*)";', source.readline())
    names_list = re.split(r'" "', names_list.groupdict().get('names'))
    return [Obj_type(name) for name in names_list]


def set_secondary_attr(param_name, attr_name, obj_list):
    new_attr = re.match(r'param '+param_name+' := "(?P<obj_name>.*)"\s+(?P<attr>\d+)',  source.readline())
    while new_attr is None:
        new_attr = re.match(r'param '+param_name+' := "(?P<obj_name>.*)"\s+(?P<attr>\d+)', source.readline())
    attr_list = [new_attr]
    new_attr = re.match(r'\s+"(?P<obj_name>.*)"\s+(?P<attr>\d+)', source.readline())
    while new_attr is not None:
        attr_list.append(new_attr)
        new_attr = re.match(r'\s+"(?P<obj_name>.*)"\s+(?P<attr>\d+)', source.readline())
    for o, a in zip(obj_list, attr_list):
        setattr(o, attr_name, int(a.groupdict().get('attr')))


with open('test.dat') as source:
    # Get students name list
    students = get_names('ETU', Etudiant)

    # Get establishment name list
    etas = get_names('ETA', Establishment)

    # Get establishments' capacities
    set_secondary_attr('capa', 'capacity', etas)
    print([o.capacity for o in etas])

    # Get students' ranks
    set_secondary_attr('rank_etu', 'rank', students)
    print([o.rank for o in students])
