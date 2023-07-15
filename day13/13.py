from functools import reduce

f = open("input")
arrival_time = int(f.readline().strip())
buses = [int(s) if s != "x" else "x" for s in f.readline().strip().split(",")]

# Part 1
def waiting_time(bus_number, arrival_time):
    r = arrival_time % bus_number
    if r == 0: 
        return r
    else:
        return bus_number - r

real_buses = [bus for bus in buses if bus != "x"]
buses_and_waiting_time = [(bus, waiting_time(bus, arrival_time)) for bus in real_buses]
(bus, time) = min(buses_and_waiting_time, key=lambda x: x[1])
print(bus * time)

# Part 2. Chinese Remainder Theorem! 
def solve_crt(constraints):
    # Solve CRT, given a list of constraints (p_i, n_i), meaning that the answer is n_i mod p_i
    # Assumes the p_i are all prime and distinct. The answer will be mod p_1p_2...p_k.
    P = reduce(lambda x, y: x*y, [p for (p, _n) in constraints])
    result = 0

    for (p, n) in constraints:
        X = n * (P // p) * pow(P // p, -1, p)
        result += X
    result %= P
    return result

constraints = []
for i, bus in enumerate(buses):
    if bus != "x":
        constraints.append((bus, -1 * i))
X = solve_crt(constraints)
print(X)
