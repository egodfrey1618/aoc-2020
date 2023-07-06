import re

# Parse the passports!
passports = []
blocks = open("input").read().strip().split("\n\n")

for block in blocks:
    passport = {}
    lines = block.split("\n")
    for line in lines:
        matches = re.findall("([a-z]{3}):([^ ]*)", line)
        for (key, value) in matches:
            # Hopefully no passport has the same key mentioned twice?
            if key in passport: assert False
            passport[key] = value
    passports.append(passport)

def int_or_none(s):
    try:
        n = int(s)
        return n
    except:
        return None

# Validate the passports!
def validate(passport, validate_data=False):
    keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for key in keys:
        if key not in passport:
            # A required key is missing
            return False

        if validate_data:
            data = passport[key]
            if key == "byr":
                year = int_or_none(data)
                if year is None: return False
                if year < 1920 or year > 2002: return False
            if key == "iyr":
                year = int_or_none(data)
                if year is None: return False
                if year < 2010 or year > 2020: return False
            if key == "eyr":
                year = int_or_none(data)
                if year is None: return False
                if year < 2020 or year > 2030: return False
            if key == "hgt":
                number = int_or_none(data[:-2])
                if number is None: return False
                ending = data[-2:]
                if ending not in ["cm", "in"]: return False
                if ending == "cm" and (number < 150 or number > 193): return False
                if ending == "in" and (number < 59 or number > 76): return False
            if key == "hcl":
                if data[0] != "#": return False
                rest = data[1:]
                if not re.findall("^[0-9a-f]{6}$", rest): return False
            if key == "ecl":
                if data not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]: return False
            if key == "pid": 
                if len(data) != 9: return False
                if int_or_none(data) is None: return False
    return True

print(len([p for p in passports if validate(p, validate_data=False)]))
print(len([p for p in passports if validate(p, validate_data=True)]))
