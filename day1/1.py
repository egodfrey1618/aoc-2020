nums = [int(x) for x in open("input").read().strip().split("\n")]
nums = set(nums)

# Part 1
for n in nums:
    other = 2020 - n
    if other in nums:
        print(n, other, n * other)

# Part 2
# Only 200 lines in the file, so O(n^2) isn't too bad
import itertools

for (p, q) in itertools.combinations(nums, 2):
    other = 2020 - p - q
    if other != p and other != q and other in nums:
        print(p, q, other, p*q*other)
