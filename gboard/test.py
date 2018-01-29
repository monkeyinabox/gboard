from gboard.infrastructure import Snapshot, Domain


d1 = Domain.query.get(1)
d2 = Domain.query.get(2)
s = Snapshot()
s.comapre(d1,d2)