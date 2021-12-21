#! /usr/bin/env python3

def load_food():
	with open('input.txt', 'r') as f:
		for line in f:
			tokens = line.split(' (contains ')
			ingredients = set(tokens[0].split())
			allergens = set(tokens[1].strip(')\n').split(', '))
			yield ingredients, allergens

ingredients_with_allergens = set([])
all_ingredients = []
known_allergens = {}
allergens_candidates = {}

for ingredients, allergens in load_food():
	for allergen in allergens:
		if allergen not in allergens_candidates:
			allergens_candidates[allergen] = ingredients
		else:
			allergens_candidates[allergen] = allergens_candidates[allergen] & ingredients
	all_ingredients.append(ingredients)

while len(allergens_candidates) > 0:
	for a, i in list(allergens_candidates.items()):
		if len(i) == 1:
			known_allergens[a] = i
			ingredients_with_allergens = ingredients_with_allergens | i
			del allergens_candidates[a]

	for i in allergens_candidates.values():
		i -= ingredients_with_allergens

count = 0
for ingredients in all_ingredients:
	count += len(ingredients - ingredients_with_allergens)

print(count)

result = [ v.pop() for _, v in sorted(known_allergens.items()) ]

print(','.join(result))

