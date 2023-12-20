#! /usr/bin/env python3

from run import load_data, Circuit

c = Circuit(load_data('input.txt'))

import graphviz

f = graphviz.Digraph('graph', filename='graph.dv')

for name, (t, lst) in c.modules.items():
	if t == '%':
		f.node(name, name, shape='circle')
	else:
		f.node(name, name, shape='square', style='filled', color='lightgrey')

for name, (t, lst) in c.modules.items():
	for i, l in enumerate(lst):
		f.edge(name, l, str(i))

f.render('graph', view=True)
