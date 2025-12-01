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