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

if __name__ == "__main__":
    constants = ['Anna', 'Bob']
    predicates = ['Smokes/1', 'Friends/2']
    ground_atoms = get_all_ground_atoms(constants, predicates)
    print(ground_atoms)