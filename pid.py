import matplotlib.pyplot as plt
import random
import json
import sys

random_number = random.uniform(0.8, 1.0)

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
vr = [0.0]
Fg = [m*g]
Fd = [0.0]

N = int(tsim/Tp) +1

#regulator PID un
v_min = 0.0
v_max = 1.0
u_min = 0.0
u_max = 5.0

kp = 0.1
Ti = 10
Td = 2
kp = float(sys.argv[2])
Ti = float(sys.argv[3])
Td = float(sys.argv[4])
zadana = 50
zadana = float(sys.argv[1])

u_PID = [0.0]
e_n = [zadana-h[-1]]

for n in range(1, N):
    
    t.append(n*Tp)
    Fd.append(0.5*pa*vr[-1]**2*Cd*A)
    v.append(((v_max - v_min)/(u_max - u_min))*(u_PID[-1]-u_min)+v_min)
    vr.append(v[-1]*random_number)
    h.append(min(max(Tp*(Fd[-1]-Fg[-1])/m+h[-1], h_min), h_max))
    Fg.append(m*g)
    e_n.append(zadana - h[-1])
    u_PID.append(kp* (e_n[-1] + (Tp/Ti*sum(e_n) + (Td * (e_n[-1] - e_n[-2]) / (t[-1] - t[-2])))))

try:
    with open("pid.json", "r") as f:
        old_data = json.load(f)
except FileNotFoundError:
    old_data = []

if not isinstance(old_data, list):
    old_data = []

data = {
    "time": t,
    "distance": h,
    "zadana": zadana,
    "kp": kp,
    "ti": Ti,
    "td": Td,
}

old_data.append(data)
old_data = old_data[-2:]

with open("pid.json", "w") as f:
    json.dump(old_data, f)