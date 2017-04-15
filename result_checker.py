import re
import unittest


class Student(object):
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


class TestAPBSimulatorResult(unittest.TestCase):

    @staticmethod
    def get_names(set_name, Obj_type, source_file):
        r_exp = re.compile(r'set '+set_name+' := "(?P<names>.*)"\s?;')
        names_list = re.match(r_exp, source_file.readline())
        while names_list is None:
            names_list = re.match(r_exp, source_file.readline())
        names_list = re.split(r'" "', names_list.groupdict().get('names'))
        return [Obj_type(name) for name in names_list]

    @staticmethod
    def set_secondary_attr(param_name, attr_name, obj_list, source_file):
        r_exp = re.compile(r'param '+param_name+' :=\s+"(?P<obj_name>.*)"\s+(?P<attr>\d+)')
        new_attr = re.match(r_exp,  source_file.readline())
        while new_attr is None:
            new_attr = re.match(r_exp, source_file.readline())
        attr_list = [new_attr]
        r_exp = re.compile(r'\s+"(?P<obj_name>.*)"\s+(?P<attr>\d+)')
        new_attr = re.match(r_exp, source_file.readline())
        while new_attr is not None:
            attr_list.append(new_attr)
            new_attr = re.match(r_exp, source_file.readline())
        for o, a in zip(obj_list, attr_list):
            setattr(o, attr_name, int(a.groupdict().get('attr')))

    @classmethod
    def setUpClass(cls):
        with open('projet1.dat') as source:
            # Get students name list
            cls.students = cls.get_names('ETU', Student, source)

            # Get establishment name list
            cls.etas = cls.get_names('ETA', Establishment, source)

            # Get establishments' capacities
            cls.set_secondary_attr('capa', 'capacity', cls.etas, source)

            # Get students' ranks
            cls.set_secondary_attr('rank_etu', 'rank', cls.students, source)

            # Get students' ranking by establishment
            while re.match(r'param rank_eta :', source.readline()) is None:
                pass
            reg = re.compile('\s+"(?P<stu_name>.*)"(?P<all_ranks>(?:\s+-?\d+)+)')
            for s in cls.students:
                ranks = re.match(reg, source.readline())
                for r, eta in zip(ranks.groupdict().get('all_ranks').split(), cls.etas):
                    if r != '-1':
                        s.eta_ranking[eta] = int(r)

        with open('projet1.out') as source:
            source.readline()
            source.readline()

            # Get students' allotment
            reg = re.compile(r'^\s+(.+)\n')
            for stu in cls.students:
                source.readline()
                eta_name = re.sub(reg, r'\1', source.readline())
                stu.establishment = next(e for e in cls.etas if e.name == eta_name)

            source.readline()
            source.readline()
            source.readline()
            source.readline()

            # Get establishments' students
            reg = re.compile(r'^\t((?:[^\t\n]+\t?)*)\n')
            for eta in cls.etas:
                source.readline()
                try:
                    eta.students = list(map(lambda s_name: next(st for st in cls.students if st.name == s_name),
                                        re.findall(reg, source.readline())[0].split('\t')))
                except IndexError:
                    pass

    def test_student_has_one_eta(self):
        for s in self.students:
            self.assertIsNotNone(s.establishment)

    def test__student_eta_in_eta_choices(self):
        for s in self.students:
            self.assertIn(s.establishment, s.eta_ranking.keys())


if __name__ == '__main__':
    unittest.main()
