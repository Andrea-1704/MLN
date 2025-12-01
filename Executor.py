from Rules import MLNRule, rule_friends_logic, rule_smokes_logic
from Utils import get_all_ground_atoms, un_normalized_world_probability, compute_partition_function, extract_constants_from_world, compute_query_probability

if __name__ == "__main__":
    my_mln = [
        MLNRule(2.0, rule_friends_logic, "Friendships_smokes_correlation"),
        MLNRule(0.5, rule_smokes_logic, "Smokes")
    ]
    example_world = {
        "Friends(Anna,Bob)": True,
        "Smokes(Anna)": True,
        "Smokes(Bob)": False,
        "Friends(Bob,Charlie)": True,
        "Smokes(Charlie)": True
    }

    weight = un_normalized_world_probability(example_world, my_mln)
    partition_function = compute_partition_function(my_mln, get_all_ground_atoms(['Anna', 'Bob', 'Charlie'], ['Smokes/1', 'Friends/2']))
    prob = weight / partition_function

    print(f"Probability of the example world: {prob}")
    print(f"Partition function Z: {partition_function}")
    target_query = "Smokes(Anna)"
    my_constants = ['Anna', 'Bob', 'Charlie']
    my_predicates = ['Smokes/1', 'Friends/2']
    prob = compute_query_probability(target_query, my_constants, my_predicates, my_mln)
    print(f"The probability that {target_query} is True is: {prob:.4f}")

    target_query = "Friends(Anna,Anna)"
    prob = compute_query_probability(target_query, my_constants, my_predicates, my_mln)
    print(f"The probability that {target_query} is True is: {prob:.4f}")