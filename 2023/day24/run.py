#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip('\n')
			t = line.split(' @ ')
			yield Coord(*tuple(map(int, t[0].split(', ')))), Coord(*tuple(map(int, t[1].split(', '))))

# Part One

from dataclasses import dataclass
from itertools import combinations


@dataclass
class Coord:
	x: int
	y: int
	z: int

def intersection2d(a, av, b, bv):
	dx = b.x - a.x
	dy = b.y - a.y
	det = bv.x * av.y - bv.y * av.x
	if det != 0:
		u = (dy * bv.x - dx * bv.y) / det
		v = (dy * av.x - dx * av.y) / det
		if u >= 0 and v >= 0:
			return Coord(a.x + u * av.x, b.y + v * bv.y, 0)
	return None

min_c, max_c = 200000000000000, 400000000000000

total = 0

for (a, av), (b, bv) in combinations(load_data('input.txt'), 2):
	i = intersection2d(a, av, b, bv)
	if i is None:
		continue
	if min_c <= i.x <= max_c and min_c <= i.y <= max_c:
		total += 1

print(total)


# Part Two

import numpy as np
from scipy.optimize import minimize
from sympy import Rational

def distance_between_3d_lines(A1, D1, A2, D2):
    """
    A1, A2: Points on the two lines (numpy arrays of shape (3,))
    D1, D2: Direction vectors of the two lines (numpy arrays of shape (3,))
    
    Returns: Shortest distance between the two lines
    """
    
    # Vector between the points on the two lines
    B = A2 - A1

    # Cross product of the two direction vectors
    D1_cross_D2 = np.cross(D1, D2)

    # If the direction vectors are parallel (cross product is zero vector)
    if np.linalg.norm(D1_cross_D2) == 0:
        # If parallel, distance is the projection of B onto a vector perpendicular to the direction
        proj_B_on_D1 = np.dot(B, D1) / np.dot(D1, D1) * D1
        distance = np.linalg.norm(B - proj_B_on_D1)
    else:
        # Otherwise, find the projection of B onto the normal vector (the cross product of D1 and D2)
        distance = np.abs(np.dot(B, D1_cross_D2)) / np.linalg.norm(D1_cross_D2)

    return distance


def objective_function(params, lines):
	P = params[:3]
	d = params[3:]

	total_distance = 0
	for P1, d1 in lines[:4]:
		P1 = np.array(P1[:3], dtype=np.float64)
		d1 = np.array(d1[:3], dtype=np.float64)
		total_distance += distance_between_3d_lines(P1, d1, P, d)**2

	return total_distance

def find_best_intersecting_line(lines):
	initial_guess = 200 * np.random.rand(6).astype(np.float64)

	result = minimize(objective_function, initial_guess, args=(lines,), options=dict(maxiter=1e6, verbose=0, gtol=1e-57, xtol=1e-57), method="trust-constr") # , ftol=1e-15

	if result.success:
		P_opt = result.x[:3]
		d_opt = result.x[3:]
		return P_opt, d_opt
	else:
		raise ValueError("Optimization failed")

lines = np.array([ [( a.x, a.y, a.z ), ( av.x, av.y, av.z )] for a, av in load_data('input.txt') ])

lines_e_minus_12 = lines.copy().astype(np.float64)
lines_e_minus_12[:,0,:] *= 1e-12

p, d = find_best_intersecting_line(lines_e_minus_12)
#print(f"The best fitting line has point: {p} and direction: {d}")

def find_integer_d(d):

	tries = []

	for t in range(1, 1000):
		td = np.array([t, t * d[1] / d[0], t * d[2] / d[0]])
		id = np.round(td)
		err = sum((td - id) ** 2)
		tries.append( (err, *id) )

	return np.round(sorted(tries)[0][1:])

d = find_integer_d(d).astype(int)

#print(f"integer d={d}")

p0 = np.array(list(map(Rational, lines[0][0])), dtype='object')
d0 = np.array(list(map(Rational, lines[0][1])), dtype='object')
p1 = np.array(list(map(Rational, lines[1][0])), dtype='object')
d1 = np.array(list(map(Rational, lines[1][1])), dtype='object')

cross = np.cross(d1, d)

term_d = np.sum(-p1 * cross)

t0 = -(np.sum(p0 * cross) + term_d) / np.sum(d0 * cross)

c0 = p0 + t0 * d0

origin = c0 - t0 * d

print(sum(origin))

