import matplotlib.pyplot as plt
from pprint import pprint
from fuzzy_logic.terms import Term
from fuzzy_logic.variables import FuzzyVariable, SugenoVariable, LinearSugenoFunction
from fuzzy_logic.sugeno_fs import SugenoFuzzySystem
from fuzzy_logic.mf import TriangularMF
import json
import sys

#parametry procesu
Cd = 1.17
m = 0.003
pa =  1.225
A = 0.0025
g = 9.8

h_min = 0.0
h_max = 100.0

#ustawienia symulacji
Tp = 0.1
tsim = 1000
h = [0.0]
t= [0.0]
v = [0.0]
Fg = [m*g]
Fd = [0.0]
vx = [0.0]

N = int(tsim/Tp) +1

zadana = 60
zadana = float(sys.argv[1])
t1: Term = Term('NB', TriangularMF(-h_max, -h_max, -h_max/8))
t2: Term = Term('NS', TriangularMF(-h_max, -h_max/8, 0))
t3: Term = Term('Z', TriangularMF(-h_max/10, 0, h_max/10))
t4: Term = Term('PS', TriangularMF(0, h_max/8, h_max))
t5: Term = Term('PB', TriangularMF(h_max/8, h_max, h_max))

e: FuzzyVariable = FuzzyVariable('e', -h_max, h_max, t1, t2, t3, t4, t5)

u: SugenoVariable = SugenoVariable(
    'u',
    LinearSugenoFunction('NB', {e: -1}, -1),
    LinearSugenoFunction('NS', {e: -0.5}, -0.5),
    LinearSugenoFunction('Z', {e: 0}, 0),
    LinearSugenoFunction('PS', {e: 0.5}, 0.5),
    LinearSugenoFunction('PB', {e: 1}, 1)
)

FS: SugenoFuzzySystem = SugenoFuzzySystem([e], [u])
FS.rules.append(FS.parse_rule('if (e is NB) then (u is NB)'))
FS.rules.append(FS.parse_rule('if (e is NS) then (u is NS)'))
FS.rules.append(FS.parse_rule('if (e is Z) then (u is Z)'))
FS.rules.append(FS.parse_rule('if (e is PS) then (u is PS)'))
FS.rules.append(FS.parse_rule('if (e is PB) then (u is PB)'))

e_n = [h_max - h[-1]]
result = FS.calculate({e: e_n[-1]})
u_n = [result[u]]

for n in range(1, N):
    t.append(n*Tp)
    Fd.append(0.5*pa*v[-1]**2*Cd*A)
    vx.append(v[-1]-Fd[-1])
    v.append(u_n[-1])
    h.append(min(max(Tp*(vx[-1]-Fg[-1])/g+h[-1], h_min), h_max))
    Fg.append(m*g)
    e_n.append(zadana - h[-1])
    result = FS.calculate({e: e_n[-1]})
    u_n.append(result[u])


data = {
    "distance": h,
    "time" : t,
    "zadana": zadana,
}

try:
    with open("fuzzy.json", "r") as f:
        old_data = json.load(f)
except FileNotFoundError:
    old_data = []

if not isinstance(old_data, list):
    old_data = []

simulation_data = {
    "time": data["time"],
    "distance": data["distance"],
    "zadana": data["zadana"],
}

old_data.append(simulation_data)
old_data = old_data[-2:]

with open("fuzzy.json", "w") as f:
    json.dump(old_data, f)