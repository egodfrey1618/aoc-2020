nums = [int(x) for x in open("input").read().strip().split("\n")]
nums.append(0) # The charging outlet
nums.append(max(nums) + 3) # My device
nums.sort()

# Part 1, easy warm-up!
jolt_1_diffs = 0
jolt_3_diffs = 0
for i in range(1, len(nums)):
    diff = nums[i] - nums[i-1]
    assert diff <= 3
    if diff == 3: jolt_3_diffs += 1
    if diff == 1: jolt_1_diffs += 1
print(jolt_3_diffs * jolt_1_diffs)

# Part 2, the fun part! How many paths are there from start to end?
# Do this with dynamic programming - work from back to front.
paths = [None for _ in nums]
paths[-1] = 1

for n in range(-2, -1*len(nums)-1, -1):
    result = 0
    for k in range(1, 4): # Only need to search 3 steps ahead - all the adapters are unique.
        if n+k < 0 and nums[n+k] - nums[n] <= 3:
            result += paths[n+k]
    paths[n] = result
print(paths)
