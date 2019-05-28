###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always an egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """


    eggs=tuple(sorted(egg_weights, reverse=True))
    if target_weight in egg_weights:
        #if target weight is a weight in egg weights, then all we do is take that egg once and we are done
        return 1
    elif len(eggs)==1:
        #if eggs has length 1, then all that is left are eggs of weight 1 since
        #1 is always in the tuple, and the target weight will be returned
        memo[eggs[0]]=target_weight
        return target_weight
    else:
        #integer division to yield the egg count for the current egg
        egg_count=target_weight//eggs[0]
        #calculate remaining weight
        remaining = target_weight-egg_count*eggs[0]
        #add egg count to the memo
        memo[eggs[0]]=egg_count
        #recursive function call on egg and remaining weight
        #removing the highest valued weight at each call
        dp_make_weight(eggs[1:], remaining,memo)
    #return the sum of all the values of the memo: the total egg count
    return sum(memo.values())



    









# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()