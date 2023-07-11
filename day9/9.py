nums = [int(x) for x in open("input").read().strip().split("\n")]

BLOCK_SIZE = 25

# Part 1
def check_num(nums, i, BLOCK_SIZE):
    assert i >= BLOCK_SIZE
    num = nums[i]
    prefix = nums[i-BLOCK_SIZE:i]
    prefix_set = set(prefix)
    for j in prefix:
        if num-j != j and num-j in prefix_set:
            return True
    return False

for i in range(BLOCK_SIZE, len(nums)):
    if not check_num(nums, i, BLOCK_SIZE):
        target = nums[i]
        print("Part 1:", target)
        break

# Part 2
for i in range(len(nums)):
    chain = [nums[i]]
    chain_sum = nums[i] 
    j = i

    while chain_sum < target and j+1 < len(nums):
        j += 1
        chain.append(nums[j])
        chain_sum += nums[j]
    if chain_sum == target and len(chain) > 1:
        print(chain)
        print("Part 2:", min(chain) + max(chain))
