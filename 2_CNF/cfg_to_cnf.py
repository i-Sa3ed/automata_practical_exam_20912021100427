from itertools import combinations # To generate new productions

# Note: we represent epsilon by letter '-'
eps = '-'

class CFGtoCNF:
    def __init__(self, cfg):
        self.cfg = cfg
    
    def eliminate_epsilon(self, grammar):
        ### Steps of elimination:
        # 1- Identify nullable variables
        # 2- Generate new productions
        # 3- Remove epsilons

        ##
        nullables = set()
        changed = True
        while changed:
            # Keep searching for nullables
            changed = False
            for nt in grammar: # nt = non terminal
                for production in grammar[nt]:
                    # Check if all symbols are nullable, or 'e'
                    all_nullable = True
                    for symbol in production:
                        if symbol != eps and symbol not in nullables:
                            all_nullable = False
                            break
                    # (nt) is a nullable variable that should be expanded
                    if all_nullable and nt not in nullables:
                        nullables.add(nt)
                        changed = True
        ##
        new_grammar = {}
        for nt in grammar:
            # store the productions after expanding
            new_productions = set()
            for production in grammar[nt]:
                if production == eps:
                    continue # all of them will be removed later
                
                # Find all nullable indices in this production
                nullable_indices = [i for i, symbol in enumerate(production)
                                    if symbol in nullables]
                
                # Generate all possible combinations of nullable symbols
                for r in range(len(nullable_indices) + 1):
                    for indices_combination in combinations(nullable_indices, r):
                        # remove symbols at these indices
                        new_production = list(production)
                        for i in sorted(indices_combination, reverse=True):
                            del new_production[i]
                        
                        if new_production: new_productions.add(''.join(new_production))
                        else: new_productions.add(eps)

            # add the new production (convert set to list)
            new_grammar[nt] = list(new_productions) 
        
        ##
        # get the start symbol to tolerate with eps
        start_symbol = next(iter(grammar))
        for nt in new_grammar:
            if eps in new_grammar[nt]:
                if nt != start_symbol:
                    new_grammar[nt].remove(eps)
                elif len(new_grammar[nt] > 1):
                    pass # only keep if there are other productions

        return new_grammar
    ###

    def eliminate_unit_productions(self, grammar):
        ## Two steps:
        # 1- find all unit pairs, maintaining the dependency of the chain
        # 2- replace each with its expansion

        ##
        unit_pairs = {}
        for nt in grammar:
            unit_pairs[nt] = set()
            queue = [nt] # to track the chain
            while queue:
                current = queue.pop(0) # Important! maintain a BFS logic
                for production in grammar.get(current, []):
                    if len(production) == 1 and production.isupper(): # found a unit production
                        if production not in unit_pairs[nt]:
                            unit_pairs[nt].add(production)
                            queue.append(production)
        
        ##
        new_grammar = {}
        for nt in grammar:
            new_productions = set()
            
            # add all productions except the unit ones 
            for production in grammar[nt]:
                if not (len(production) == 1 and production.isupper()):
                    new_productions.add(production)
            
            # add the expansions from the unit pairs
            for unit_nt in unit_pairs[nt]:
                new_productions.update(
                    prod for prod in grammar.get(unit_nt, [])
                    if not (len(prod) == 1 and prod.isupper())
                )
            
            new_grammar[nt] = list(new_productions)
        
        ##
        return new_grammar
    ###

    def replace_terminals(self, grammar):
        # Goal: replace the mixed productions (e.g. aSb, xA)

        nt_generator = 'A' # to generate new non terminals 
        terminal_rules = {} # stores the new generated rules
        new_grammar = {}

        for nt in grammar:
            new_productions = []
            for production in grammar[nt]:
                # Check if there are terminals:
                if len(production) >= 2 and any(symbol.islower() for symbol in production):
                    new_prod = []
                    for symbol in production:
                        if symbol.islower(): # found a terminal
                            # Check if we visited before:
                            if symbol not in terminal_rules.values():
                                new_nt = nt_generator
                                terminal_rules[new_nt] = symbol
                                nt_generator = chr(ord(nt_generator) + 1)
                            else: # reuse the rule generated before 
                                new_nt = [k for k, v in terminal_rules.items() if v == symbol][0]
                            
                            new_prod.append(new_nt)
                        else:
                            new_prod.append(symbol)
                    
                    new_productions.append(''.join(new_prod))
                else:
                    new_productions.append(production) # add as it is
            
            new_grammar[nt] = new_productions
        
        # add the new terminal rules to the grammar:
        for new_nt, terminal in terminal_rules.items():
            new_grammar[new_nt] = [terminal]
        
        return new_grammar
    ###

    def break_long_rules(self, grammar):
        # Goal: breaks the long rules into multiple binary ones

        counter = 0 # for generating new non terminals (e.g. Y0, Y1)
        new_grammar = {}

        for nt in grammar:
            for production in grammar[nt]:
                # Check if it's long:
                if len(production) > 2:
                    # split the production into binary rules
                    current_nt = nt
                    remaining = production
                    while len(remaining) > 2:
                        new_nt = f"M{counter}"
                        counter += 1
                        # set an empty list if not found, then append the value to it
                        new_grammar.setdefault(current_nt, []).append(f"{remaining[0]}{new_nt}")
                        
                        current_nt = new_nt
                        remaining = remaining[1:]
                    new_grammar.setdefault(current_nt, []).append(remaining)
                else:
                    new_grammar.setdefault(nt, []).append(production)
        
        return new_grammar

    def cfg_to_cnf(self):
        # Phase 1
        result1 = self.eliminate_epsilon(self.cfg)

        # Phase 2
        result2 = self.eliminate_unit_productions(result1)

        # Phase 3
        result3 = self.replace_terminals(result2)

        # Phase 4
        final = self.break_long_rules(result3)
        
        return final

## Test
grammar = {
    'S': ['aSb', 'Z', eps],
    'Z': ['Y'],
    'Y': ['y'],
}
cnf = CFGtoCNF(grammar)
print(cnf.cfg_to_cnf())
