from collections import namedtuple
import re

Item = namedtuple("Item", ["amount", "colour"])
Rule = namedtuple("Rule", ["colour", "items"])
Problem = namedtuple("Problem", ["all_colours", "rules_by_colour", "rules_by_item_colour"])

def parse_problem(s):
    all_colours = set()
    rules_by_colour = {}
    rules_by_item_colour = {}

    for line in s:
        if line == "": continue
        prefix = re.findall("^([a-z]+ [a-z]+) bags contain ", line)
        assert prefix
        colour = prefix[0]
        line = line[len(colour + " bags contain "):]

        if line == "no other bags.":
            # This bag has to be empty.
            items = []
        else:
            # This bag has to be non-empty. 
            bags = re.findall("([0-9]+) ([a-z]+ [a-z]+) bags?", line)
            assert bags, line
            items = [Item(amount=int(b[0]), colour=b[1]) for b in bags]
        rule = Rule(colour=colour, items=items)
        all_colours.add(colour)
        rules_by_colour[colour] = rule
        for item in items:
            if item.colour not in rules_by_item_colour: 
                rules_by_item_colour[item.colour] = []
            rules_by_item_colour[item.colour].append(rule)
    return Problem(all_colours=all_colours, rules_by_colour=rules_by_colour, rules_by_item_colour=rules_by_item_colour)

def find_all_colours_that_can_contain(problem, colour):
    """
    Find all colours that can contain a given colour. This is essentially a backwards search through
    the graph. I haven't really specified in what order. 
    """
    to_process = {colour}
    processed = set()
    result = []

    while to_process:
        next_ = to_process.pop()
        processed.add(next_)
        containing_rules = problem.rules_by_item_colour.get(next_, [])

        # For each colour that can directly contain this one, need to recursively check it.
        for rule in containing_rules:
            if rule.colour not in processed and rule.colour not in to_process:
                to_process.add(rule.colour)
                result.append(rule.colour)
    return result

def find_total_bags_that_this_bag_must_contain(problem, colour):
    # This is recursive, so isn't really reasonable in Python (you'd blow up the stack limit)
    # But for the size of graph here, turns out that this is OK, and it was easier to write
    # I'm also not memoizing this, so am redoing work, but turns out to be fine for the input.
    # 
    # "Proper" way to do this would be to reverse topologically sort the graph, and then it's O(n)
    # time to do one sweep over the graph to compute the cost of each one.
    rule = problem.rules_by_colour[colour]
    result = sum(item.amount * (1 + find_total_bags_that_this_bag_must_contain(problem, item.colour)) for item in rule.items)
    return result

s = open("input","r").read().split("\n")
problem = parse_problem(s)
X = find_all_colours_that_can_contain(problem, "shiny gold")
print(len(X))
Y = find_total_bags_that_this_bag_must_contain(problem, "shiny gold")
print(Y)
