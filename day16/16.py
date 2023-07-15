import re
from functools import reduce

# Lots of parsing for this one!
fields = {}

f = open("input","r")
# Read until the first blank line
while (line := f.readline().strip()) != "":
    match = re.findall("^(.*): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$", line)
    assert len(match) == 1
    (name, x1, y1, x2, y2) = match[0]
    (x1, y1, x2, y2) = map(int, (x1, y1, x2, y2))
    fields[name] = ((x1, y1), (x2, y2))

assert f.readline().strip() == "your ticket:"
my_ticket = [int(x) for x in f.readline().strip().split(",")]

assert f.readline().strip() == ""
assert f.readline().strip() == "nearby tickets:"
nearby_tickets = []
for line in f:
    nearby_tickets.append([int(x) for x in line.strip().split(",")])

# Part 1
def bounds_match_value(bounds, value):
    ((x1, y1), (x2, y2)) = bounds
    return (value >= x1 and value <= y1) or (value >= x2 and value <= y2)

def value_matches_any_field(value):
    for bounds in fields.values():
        if bounds_match_value(bounds, value): return True
    return False

total_invalid = 0
for ticket in nearby_tickets:
    for v in ticket:
        if not value_matches_any_field(v): total_invalid += v
print(total_invalid)

# Part 2!
nearby_tickets = [t for t in nearby_tickets if all(value_matches_any_field(v) for v in t)]

# Loop over each ticket / position number, and filter out any fields that would be impossible.
field_number_to_possible_fields = {}
for field_number in range(len(nearby_tickets[0])): 
    possible_fields = set(fields.keys())

    def check_ticket(ticket):
        impossible_fields = []
        for field in possible_fields:
            if not bounds_match_value(fields[field], ticket[field_number]):
                impossible_fields.append(field)

        for f in impossible_fields: possible_fields.remove(f)

    for ticket in nearby_tickets: check_ticket(ticket)
    check_ticket(my_ticket)
    field_number_to_possible_fields[field_number] = possible_fields

# Now we have a matching problem. How do we assign fields to tickets? In general, this can be solved with a 
# flow algorithm.
# But we can do an easier thing first. Any field numbers where we've uniquely found the ticket number - we 
# can fix that, and filter that out from any others.
processed = set()
unique_matches = {}
while True:
    new_unique_matches = []
    for field_number, possible_names in field_number_to_possible_fields.items():
        if field_number not in processed and len(possible_names) == 1:
            name = list(possible_names)[0]
            new_unique_matches.append((field_number, name))
            unique_matches[field_number] = name

    for (field_number, name) in new_unique_matches:
        processed.add(field_number)
        for other_field, possible_names in field_number_to_possible_fields.items():
            if other_field != field_number and name in possible_names: 
                # Because we've uniquely mapped this name to another field, we can get rid of it
                possible_names.remove(name)

    if new_unique_matches == []:
        break

if len(unique_matches) == len(my_ticket):
    print("yay, successfully matched all fields")
    print(reduce(lambda x, y: x*y, [t for i, t in enumerate(my_ticket) if unique_matches[i].startswith("departure")]))

