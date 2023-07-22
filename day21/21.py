import re

problem_case = []

f = open("input")
for line in f:
    ingredients = re.findall("^(.*) \(contains", line)[0].split(" ")
    allergens = re.findall("\(contains (.*)\)$", line)[0].split(" ")
    allergens = ["".join(c for c in s if c != ",") for s in allergens]
    problem_case.append((ingredients, allergens))

allergen_to_possible_ingredient = {}

# Loop through each problem case, finding the set of ingredients that might be the one for the allergen.
for (ingredients, allergens) in problem_case:
    for allergen in allergens:
        if allergen not in allergen_to_possible_ingredient:
            allergen_to_possible_ingredient[allergen] = set(ingredients)
        else:
            allergen_to_possible_ingredient[allergen] &= set(ingredients)

ingredients_that_might_contain_an_allergen = set()
for v in allergen_to_possible_ingredient.values():
    ingredients_that_might_contain_an_allergen |= v

# Part 1: Count up how many times an ingredient that is definitely safe appears.
count = 0
for (ingredients, allergens) in problem_case:
    count += len([i for i in ingredients if i not in ingredients_that_might_contain_an_allergen])
print(count)

# Part 2: Now figure out which allergen is which ingredient!
# Similar to day 16, this should be a flow algorithm, but I can do something simpler.
definite_matches = {}

while allergen_to_possible_ingredient:
    for allergen in list(allergen_to_possible_ingredient.keys()):
        possible_ingredients = [i for i in allergen_to_possible_ingredient[allergen] if i not in definite_matches]

        if len(possible_ingredients) == 1:
            definite_matches[possible_ingredients[0]] = allergen
            allergen_to_possible_ingredient.pop(allergen)
        else:
            allergen_to_possible_ingredient[allergen] = possible_ingredients

allergen_to_ingredient = {v:k for (k, v) in definite_matches.items()}
print(",".join(allergen_to_ingredient[allergen] for allergen in sorted(allergen_to_ingredient.keys())))
