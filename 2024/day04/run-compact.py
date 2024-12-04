#! /usr/bin/env python3

import numpy as np

npa = lambda *s: np.array(list(map(list, s)))
swv = np.lib.stride_tricks.sliding_window_view
n_matches = lambda k: np.sum(np.all(np.logical_or(swv(input, k.shape) == k, k == '.'), axis=(2, 3)))
num = lambda k: sum( n_matches(np.rot90(k, i)) for i in range(4) )
s2k = lambda *s: num(npa(*s))

input = npa(*open('input.txt').read().splitlines())
result1 = s2k('XMAS') + s2k('X...', '.M..', '..A.', '...S')
result2 = s2k('M.S', '.A.', 'M.S')

print(result1, result2, sep='\n')
