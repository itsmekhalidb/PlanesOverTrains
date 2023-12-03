class File_Parser():
    def __init__(self):
        self._occupancy = {}
        self._pos = 0
        self._line = ""

    def get_next_token(self):
        if self._pos < len(self._line):
            token = self._line[self._pos]
            self._pos += 1
            return token
        return '\0'  # Return null character to indicate end of input

    def parse_expression(self):
        result = self.parse_term()

        while True:
            op = self.get_next_token()
            if op == "and" or op == "or":
                term = self.parse_term()
                if op == "and":
                    result = result and term
                else:
                    result = result or term
            else:
                self._pos -= 1  # Put back the character if it's not an operator
                break

        return result

    def parse_term(self):
        result = self.parse_factor()

        while True:
            op = self.get_next_token()
            if op == '!':
                result = not result
            else:
                self._pos -= 1  # Put back the character if it's not an operator
                break

        return result

    def parse_factor(self):
        token = self.get_next_token()
        if token.isalpha():
            return token.upper() == 'T'
        elif token == '(':
            result = self.parse_expression()
            if self.get_next_token() != ')':
                # Handle mismatched parentheses
                print("Error: Mismatched parentheses")
                exit(1)
            return result
        else:
            # Handle unexpected characters
            print(f"Error: Unexpected character '{token}'")
            exit(1)

    def parse(self, line: str, occupancy: dict):
        self._occupancy = occupancy
        self._line = line
        self.parse_expression()





