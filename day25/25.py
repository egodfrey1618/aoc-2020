# Diffie-Hellman!
n = 9093927
m = 11001876
p = 20201227
g = 7

i = 1
k = g
while True:
    i += 1
    k *= g
    k %= p
    if k == m or k == n:
        print("Found one of the private keys!")
        if k == m:
            print(pow(n, i, p))
        else:
            print(pow(m, i, p))
        break
