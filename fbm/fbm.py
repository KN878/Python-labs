from math import sqrt
from random import normalvariate


def fbm():
    N = 100
    W0 = 0
    tau = 0.5
    s = sqrt(tau)
    W = [W0]

    for i in range(1, N):
        W_i = W[i-1] + normalvariate(0, 1) * s
        W.append(W_i)

    print(W)


if __name__ == "__main__":
    fbm()
