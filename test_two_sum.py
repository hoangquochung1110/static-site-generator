import pytest


def two_sum(nums: list[int], target: int) -> list[int]:
    hashmap = {}
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in hashmap:
            return [i, hashmap[complement]]
        hashmap[nums[i]] = i

@pytest.mark.parametrize(
    "nums, target, result",
    [
        [[2,7,11,15], 9, [1,0]],
        [[3,2,4], 6, [2,1]],
    ]
)
def test_two_sum(nums: list[int], target: int, result: list[int]):
    assert two_sum(nums, target) == result
