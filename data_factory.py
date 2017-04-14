import random
import factory


class Etudiant(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return '"'+self.__repr__()+'"'

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def init_eta_list(self, size):
        self.eta_ranking = [-1]*size
        eta_rank = []
        for i in range(0, 6):
            r = random.randint(0, size-1)
            if r in eta_rank:
                i -= 1
                continue
            eta_rank.append(r)
        for i, r in enumerate(eta_rank):
            self.eta_ranking[r] = i+1
        return self


class Establishment(object):
    def __init__(self, name, number, capacity):
        self.name = name
        self.number = number
        self.capacity = capacity

    def __repr__(self):
        return '{} {}'.format(self.name, self.number)

    def __str__(self):
        return '"'+self.__repr__()+'"'

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())


class RandomStudentFactory(factory.Factory):
    class Meta:
        model = Etudiant

    name = factory.Faker('name', 'fr_FR')


class RandomEstablishmentFactory(factory.Factory):
    class Meta:
        model = Establishment

    name = factory.Faker('city', 'fr_FR')
    number = factory.Sequence(lambda n: n)
    capacity = 50

    @classmethod
    def _setup_next_sequence(cls):
        return 1


etas = []
for i in range(1, 100):
    eta = RandomEstablishmentFactory(capacity=random.randint(100, 300))
    etas.append(eta)
    for j in range(1, random.randint(1, 12)):
        etas.append(RandomEstablishmentFactory(name=eta.name, capacity=random.randint(100, 300)))
    RandomEstablishmentFactory.reset_sequence()
etas = set(etas)
students = set(list(map(lambda s: s.init_eta_list(len(etas)), RandomStudentFactory.build_batch(1000))))


max_eta_name = len(max([str(s) for s in etas], key=len))
max_stu_name = len(max([str(s) for s in students], key=len))

with open('projet1.dat', 'w') as dest:
    dest.write('data;\n\n')
    dest.write('/* Students list */\n')
    dest.write(' '.join(['set ETU :=']+[str(s) for s in students]+[';\n']))
    dest.write('/* Establishments list */\n')
    dest.write(' '.join(['set ETA :='] + [str(s) for s in etas] + [';\n\n']))
    dest.write('/* Capacity of establishments */\nparam capa :=   ')
    dest.write('\n\t\t\t\t'.join(['{:<{width}} {:=10d}'.format(str(s), s.capacity, width=max_eta_name) for s in etas]))
    dest.write(" ;\n\n")
    dest.write('/* General ranking of students */\nparam rank_etu :=   ')
    dest.write('\n\t\t\t\t\t'.join(['{:<{width}} {:=10d}'.format(str(s), i+1, width=max_stu_name) for i,s in enumerate(students)]))
    dest.write(" ;\n\n")
    dest.write('/* Ranking of establishments per student */\nparam rank_eta : {:{width}}'.format(' ', width=max_stu_name+3))
    dest.write(' '.join(['{:{width}}'.format(str(s), width=max_eta_name) for s in etas]+[":=\n\t\t\t\t"]))
    dest.write('\n\t\t\t\t'.join(['{:<{width}} {}'.format(str(s), ''.join(['{:^{width2}d}'.format(rank, width2=max_eta_name+1) for rank in s.eta_ranking]), width=max_stu_name) for s in students]))
    dest.write(" ;\n\nend;\n")
