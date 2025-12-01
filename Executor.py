from Rules import MLNRule, rule_friends_logic, rule_smokes_logic
from Utils import get_all_ground_atoms, un_normalized_world_probability, compute_partition_function, compute_marginal, compute_conditional_probability

if __name__ == "__main__":
    my_mln = [
        MLNRule(2.0, rule_friends_logic, "Friendships_smokes_correlation"),
        MLNRule(0.5, rule_smokes_logic, "Smokes")
    ]
    my_constants = ['Anna', 'Bob', 'Charlie']
    my_predicates = ['Smokes/1', 'Friends/2']

    target_query = "Smokes(Anna)"
    prob = compute_marginal(target_query, my_constants, my_predicates, my_mln)
    print(f"The probability that {target_query} is True is: {prob:.4f}")


    query = "Smokes(Anna)"
    conditioning_query = ["Friends(Anna,Bob)", "Smokes(Bob)"]
    #conditioning_query = ["Smokes(Anna)"]
    cond_prob = compute_conditional_probability(query, conditioning_query, my_constants, my_predicates, my_mln)
    print(f"P({query} | {conditioning_query}) = {cond_prob:.4f}")