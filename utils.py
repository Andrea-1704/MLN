import itertools
import math

def get_all_ground_atoms(constants, predicates):
    """
    This function should return all the possible ground nodes obtained by applying each predicate to every possible 
    constant.
    Input:
      constants: list ['Anna', 'Bob']
      predicates: list ['Smokes/1', 'Friends/2']
    """
    ground_atoms = set()
    for predicate in predicates:
        if "/" in predicate:
            name, arity_str = predicate.split("/")
            arity = int(arity_str)
        else:
            #it shouldn't happen
            name = predicate
            arity = 1
        
        for arguments in itertools.product(constants, repeat=arity):
            args_str = ",".join(arguments) #('Anna', 'Bob') -> "Anna,Bob".
            atom_string = f"{name}({args_str})" #this is the final name
            ground_atoms.add(atom_string)
    
    return ground_atoms

def extract_constants_from_world(world):
    """
    Given a world (dict of ground atoms to boolean values), extract the set of constants used.
    Input:
      world: dict mapping ground atoms to boolean values
    Output:
      constants: set of constants found in the ground atoms
    """
    constants = set()
    for atom in world.keys():
        if '(' in atom and ')' in atom:
            args_str = atom[atom.index('(')+1 : atom.index(')')]
            args = args_str.split(',')
            for arg in args:
                constants.add(arg.strip())
    return constants

def un_normalized_world_probability(world, mln_rules):
    """
    Compute the probability of a given world according to the MLN rules.
    Input:
      world: dict mapping ground atoms to boolean values
      mln_rules: list of MLNRule objects
    Output:
      probability: float
    """
    exponent = 0.0
    for rule in mln_rules:
        ni_x = rule.evaluate(world, constants=list(extract_constants_from_world(world)))
        exponent += rule.weight * ni_x
    
    return math.exp(exponent)

def compute_partition_function(mln_rules, ground_atoms):
    """
    Compute the partition function Z by summing over all possible worlds.
    Input:
      mln_rules: list of MLNRule objects
      ground_atoms: set of all ground atoms
    Output:
      Z: float
    """
    Z = 0.0
    ground_atom_list = list(ground_atoms)
    num_atoms = len(ground_atom_list)
    
    for i in range(2 ** num_atoms):
        world = {}
        for j in range(num_atoms):
            atom = ground_atom_list[j]
            world[atom] = (i & (1 << j)) != 0
        
        prob = un_normalized_world_probability(world, mln_rules)
        Z += prob
    
    return Z

def compute_world_scores_where_query_true(query_atom, constants, predicates, rules):
    """
    Returns a list of unnormalized scores (exponential weights) for all possible worlds 
    where the specific 'query_atom' is TRUE.
    """
    #generate all possible ground atoms (the variables of our system)
    # Example: ['Smokes(Anna)', 'Smokes(Bob)', 'Friends(Anna,Bob)', ...]
    # Sorting ensures consistent ordering for the itertools product
    all_ground_atoms = sorted(list(get_all_ground_atoms(constants, predicates)))
    scores = []
    #Generate ALL possible worlds (Cartesian product of False/True) 2^K
    for values in itertools.product([False, True], repeat=len(all_ground_atoms)):
        world = dict(zip(all_ground_atoms, values))
        #We only care about worlds where the Query is TRUE
        if world.get(query_atom, False) is True:
            score = un_normalized_world_probability(world, rules)
            scores.append(score)
    return scores

def compute_marginal(query_atom, constants, predicates, rules):
    """
    Computes the marginal probability P(Query).
    Formula: P(Q) = (Sum of weights of worlds where Q is True) / Z
    """
    # Sum of unnormalized scores for all worlds where the query is True
    relevant_scores = compute_world_scores_where_query_true(query_atom, constants, predicates, rules)
    numerator = sum(relevant_scores)
    # Sum of unnormalized scores for ALL possible worlds (both where Q is True and False)
    all_ground_atoms = get_all_ground_atoms(constants, predicates)
    partition_function_Z = compute_partition_function(rules, all_ground_atoms)
    #This is a trick not to compute the Z for all the P(w).
    if partition_function_Z == 0:
        return 0.0
        
    return numerator / partition_function_Z

def compute_joint_probability(query_atoms, constants, predicates, rules):
    """
    Returns a list of unnormalized scores (exponential weights) for all possible worlds 
    where the specific 'query_atoms' are TRUE.
    """
    all_ground_atoms = sorted(list(get_all_ground_atoms(constants, predicates)))
    scores = []
    #Generate ALL possible worlds (Cartesian product of False/True)
    for values in itertools.product([False, True], repeat=len(all_ground_atoms)):
        world = dict(zip(all_ground_atoms, values))
        #We only care about worlds where the Query is TRUE
        if all(world.get(atom, False) is True for atom in query_atoms):
            score = un_normalized_world_probability(world, rules)
            scores.append(score)
    return scores

def compute_conditional_probability(query, conditioning_facts, constants, predicates, rules):
    all = conditioning_facts + [query]
    numerator_scores = compute_joint_probability(all, constants, predicates, rules)
    numerator = sum(numerator_scores)

    denominator_scores = compute_joint_probability(conditioning_facts, constants, predicates, rules)
    denominator = sum(denominator_scores)
    if denominator == 0:
        return 0.0
    #here i can avoid to compute z
    return numerator / denominator
    