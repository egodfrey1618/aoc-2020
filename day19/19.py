"""
This was fun! I think I probably did this in a slightly more general way - I did the dynamic programming
method that I remember reading in Skiena's book for parsing grammers. I suspect there are smarter things
you can do here - e.g. some sort of preprocessing on the rules that checks the easier cases faster. But
this worked well enough.
"""
import time

class Rule(object):
    def __init__(self, *, rule_id, tokens):
        self.rule_id = rule_id
        # tokens is a list of lists of tokens
        self.tokens = tokens

def parse_rule(s):
    rule_id = int(s.split(":")[0])
    options = [t.strip() for t in s.split(":")[1].split("|")]
    tokens = []
    for option in options:
        if len(option) == 3 and option[0] == "\"" and option[2] == "\"":
            # Single character
            tokens.append([option[1]])
        else:
            # Some number of ints.
            tokens.append([int(x) for x in option.split(" ")])
    return Rule(rule_id=rule_id, tokens=tokens)

def rules_match(s, rules, rule_id):
    """
    Basically the CYK algorithm for context-free grammars.
    """
    # Tries to identify, given a set of rules and a rule_id, whether that matches a string.
    cache = {}
    rules_by_id = {rule.rule_id: rule for rule in rules}

    def inner(i, j, rule_id):
        # Does s[i:j] match the given rule_id? The result of this is memoized - so this is a dynamic programming thing.
        cache_key = (i, j, rule_id)
        if cache_key in cache: return cache[cache_key]

        rule = rules_by_id[rule_id]
        result = False
        for tokens in rule.tokens:
            if len(tokens) > (j - i):
                # None of our rules allow an empty character, so we can just continue.
                continue

            if len(tokens) == 1:
                # The one token case. Check if it's a string or an int.
                token = tokens[0]
                if type(token) == str:
                    if s[i] == token and j == i + 1:
                        result = True
                        break
                    else:
                        continue
                elif type(token) == int:
                    if inner(i, j, token):
                        result = True
                        break
                    else:
                        continue
                else: assert False
            else:
                # The multiple token case. To simplify things - as it's what AoC has - let's assert these are all ints.
                # I'll also assert the length is 2 or 3, for simplicity.
                #
                # Edit: I realise afterwards I could have simplified this by turning the "3 token rules" into "2 token rules"
                # by adding more rules.
                assert all(type(t) == int for t in tokens) 
                assert len(tokens) in [2, 3]
                if len(tokens) == 2:
                    for i_ in range(i, j):
                        if inner(i, i_, tokens[0]) and inner(i_, j, tokens[1]):
                            result = True
                            break
                elif len(tokens) == 3:
                    for i_ in range(i, j):
                        if result: break
                        for j_ in range(i_, j):
                            if inner(i, i_, tokens[0]) and inner(i_, j_, tokens[1]) and inner(j_, j, tokens[2]):
                                result = True
                                break
                if result: break
        cache[cache_key] = result
        return result
    X = inner(0, len(s), rule_id)
    return X
 
rules = []
f = open("input")
while (line := f.readline().strip()) != "":
    rules.append(parse_rule(line))

strings = f.read().strip().split("\n")

# Part 1
start_ = time.time()
print(len([s for s in strings if rules_match(s, rules, 0)]))
end_ = time.time()
print(f"Did part 1 in {end_ - start_}s")

# Part 2
for rule in rules:
    if rule.rule_id == 8:
        rule.tokens = [[42], [42, 8]]
    if rule.rule_id == 11:
        rule.tokens = [[42, 31], [42, 11, 31]]
start_ = time.time()
print(len([s for s in strings if rules_match(s, rules, 0)]))
end_ = time.time()
print(f"Did part 2 in {end_ - start_}s")
