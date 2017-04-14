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
    def __init__(self, name, capacity = 0):
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return '"'+self.__repr__()+'"'


with open('test.dat') as source:
    #Get students name list
    students = re.match(r'set ETU := "(?P<names>.*)";', source.readline())
    while students is None:
        students = re.match(r'set ETU := "(?P<names>.*)";', source.readline())
    students_names = re.split(r'" "', students.groupdict().get('names'))
    students = [Etudiant(name) for name in students_names]

    #Get establishment name list
    etas = re.match(r'set ETA := "(?P<attr>.*)";', source.readline())
    while etas is None:
        etas = re.match(r'set ETA := "(?P<attr>.*)";', source.readline())
    etas_names = re.split(r'" "', etas.groupdict().get('attr'))
    etas = [Establishment(name) for name in etas_names]

    #Get establishments' capacities
    capa = re.match(r'param capa := "(?P<eta>.*)"\s+(?P<capa>\d+)',  source.readline())
    while capa is None:
        capa = re.match(r'param capa := "(?P<eta>.*)"\s+(?P<capa>\d+)', source.readline())
    capas = [capa]
    capa = re.match(r'\s+"(?P<eta>.*)"\s+(?P<capa>\d+)', source.readline())
    while capa is not None:
        capas.append(capa)
        capa = re.match(r'\s+"(?P<eta>.*)"\s+(?P<capa>\d+)', source.readline())
    for e, c in zip(etas, capas):
        e.capacity = c.groupdict('capa')
    print([e.capacity for e in etas])

    #Get students' rankg
    rank = re.match(r'param rank_etu := "(?P<stu>.*)"\s+(?P<rank>\d+)',  source.readline())
    while capa is None:
        capa = re.match(r'param capa := "(?P<eta>.*)"\s+(?P<capa>\d+)', source.readline())
    capas = [capa]
    capa = re.match(r'\s+"(?P<eta>.*)"\s+(?P<capa>\d+)', source.readline())
    while capa is not None:
        capas.append(capa)
        capa = re.match(r'\s+"(?P<eta>.*)"\s+(?P<capa>\d+)', source.readline())
    for e, c in zip(etas, capas):
        e.capacity = c.groupdict('capa')
    print([e.capacity for e in etas])

