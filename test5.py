"""
Proof-of-concept for tagging system.

P1 is embedding for benchmark point 1 (e.g. "dark")
P2 is embedding for benchmark point 2 (e.g. "bright")

X is embedding of current sample

factor goes from 0 to 1 and interpolates between P1 and P2

e.g factor 0.1 means very dark sound, factor 0.3 pretty dark and so on

More fluid tag alignment than Splice.
"""

import matplotlib.pyplot as plt
import numpy as np


P1 = np.array([-2, -2])
P2 = np.array([4, 2])

X = np.array([-2, 1])

delta = P2 - P1  # vector distance
deltadiff = np.sqrt(delta.dot(delta))  # scalar distance between P1 and P2


lerps = [
    P1 + q * delta for q in np.linspace(0, 1, 10)
]  # some points on the line between P1 and P2


x_to_p1 = P1 - X
x_to_p2 = P2 - X

factor = np.sqrt(x_to_p1.dot(x_to_p1)) - np.sqrt(x_to_p2.dot(x_to_p2))
factor /= deltadiff * 2
factor += 0.5

POINT = P1 + delta * factor


points = [P1, P2, X, *lerps, POINT]
plt.scatter([p[0] for p in points], [p[1] for p in points])

plt.show()
