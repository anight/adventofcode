#! /usr/bin/env python3

def load_data(filename):
	with open(filename, 'r') as f:
		template = f.readline().strip()
		rules = {}
		for line in f:
			line = line.strip()
			if line == '':
				continue
			t = line.split(' -> ')
			rules[t[0]] = t[1]
		return template, rules

# Part One

template, rules = load_data('input.txt')

def onestep(template, rules):
	new_template = ''
	for c in template:
		if new_template == '':
			new_template += c
			continue
		i = rules[new_template[-1] + c]
		new_template += i + c
	return new_template

for _ in range(10):
	template = onestep(template, rules)

result = sorted( template.count(c) for c in set(template) )

print(result[-1] - result[0])

# Part Two

template_pairs = {}
template_chars = {}
prev_c = None
for c in template:
	if c not in template_chars:
		template_chars[c] = 1
	else:
		template_chars[c] += 1
	if prev_c is not None:
		key = prev_c + c
		if key not in template_pairs:
			template_pairs[key] = 1
		else:
			template_pairs[key] += 1
	prev_c = c

def onestep2(template_pairs, template_chars, rules):
	new_template_pairs = {}
	new_template_chars = template_chars.copy()
	for k, v in template_pairs.items():
		i = rules[k]
		new_template_chars[i] += v
		for key in (k[0] + i, i + k[1]):
			if key not in new_template_pairs:
				new_template_pairs[key] = v
			else:
				new_template_pairs[key] += v
	return new_template_pairs, new_template_chars

for _ in range(40 - 10):
	template_pairs, template_chars = onestep2(template_pairs, template_chars, rules)

result = sorted( v for v in template_chars.values() )

print(result[-1] - result[0])

