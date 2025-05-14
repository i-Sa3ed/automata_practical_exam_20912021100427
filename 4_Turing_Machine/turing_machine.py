class TuringMachine:
    def __init__(self, binary_number):
        # generate the TM components: tape, head, states and transitions
        self.tape = list(binary_number)
        self.head = len(self.tape) - 1  # start from the LSB
        self.state = 'scan'
        # We have 3 transitions: scan, increment, and finally halt
        self.transitions = {
            'scan': {
                # Possible symbols: 0, 1, and Blank(-)
                # (new_state, write_symbol, move)
                '0': ('increment', '1', 0), # Flip 0 to 1 and halt (no move)
                '1': ('scan', '0', -1), # Flip 1 to 0 and continue scanning
                '-': ('increment', '1', 0) # Flip Blank to 1 and halt
            }
        }
    
    def step(self):
        # Termination stete
        if self.state == 'halt':
            return False
        
        # Get the symbol and validate it
        symbol = self.tape[self.head] if self.head >= 0 else '-'
        if symbol not in self.transitions[self.state]:
            raise ValueError(f'Invalid symbol found in the input: {symbol}')
        
        # Do the step:
        new_state, write_symbol, move = self.transitions[self.state][symbol]
        if self.head >= 0:
            self.tape[self.head] = write_symbol
        else:
            self.tape = ['1'] + self.tape # Reach the tape edge => append '1' at the beginning
        
        self.head += move
        self.state = 'halt' if new_state == 'increment' else new_state

        return True

    def run(self):
        while self.step():
            pass
        
        result = ''.join(self.tape) # Convert to string
        return result

## Test
tm = TuringMachine('1011')
print(tm.run()) # Output: 1100

tm = TuringMachine('1111')
print(tm.run()) # Output: 10000

tm = TuringMachine('0')
print(tm.run()) # Output: 1

tm = TuringMachine('')
print(tm.run()) # Output: 1