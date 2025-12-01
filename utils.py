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

class MLNRule:
    def __init__(self, weight, logic_function, name=""):
        self.weight = weight      # w_i
        self.logic = logic_function
        self.name = name

    def evaluate(self, world, constants):
        """Compute n_i(x): how many times the rule is true in this world."""
        return self.logic(world, constants)

# Rule 1: Friends(x,y) => (Smokes(x) <=> Smokes(y))
# Weight: 2.0
def rule_friends_logic(world, constants):
    """
    For all pairs (x,y):
        If Friends(x,y) is true, then check if Smokes(x) == Smokes(y)
    Count how many such implications are satisfied. It returns the ni(x) value.
    """
    count_satisfied = 0
    for x in constants:
        for y in constants:
            # Retrieve truth values from the current world
            friends_xy = world.get(f"Friends({x},{y})", False) # Default False if not present
            smokes_x = world.get(f"Smokes({x})", False)
            smokes_y = world.get(f"Smokes({y})", False)
            
            # Logic: A => B is equivalent to (NOT A) OR B
            # Here B is (smokes_x == smokes_y)
            is_satisfied = (not friends_xy) or (smokes_x == smokes_y)
            
            if is_satisfied:
                count_satisfied += 1
    return count_satisfied

# Rule 2: Smokes(x)
# Weight: 0.5
def rule_smokes_logic(world, constants):
    """
    For all x:
        Count how many Smokes(x) are true.
    It returns the ni(x) value.
    """
    count_satisfied = 0
    for x in constants:
        val = world.get(f"Smokes({x})", False)
        if val: # If true, the rule is satisfied
            count_satisfied += 1
    return count_satisfied

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