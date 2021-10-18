    # TODO: In find_main_operator(), test for multiple operators at depth 0 
    # Apply standard order of operations if multiple operators at depth 0
    # e.g. ¬A∨B should recognize ∨ as the main logical operator

class Syntax:

    @staticmethod
    def is_valid_TFL(str):
        """
        Determine if a line of text represents a valid TFL statement
        """
        
        # Lines in a `prooftext` contain a justification after the '#' symbol
        # If the line contains a justification, remove it
        line = str
        if '#' in line:
            line = Syntax.remove_justification(line)

        # Strip all whitespace from the line
        line.replace(" ", "")

        # Verify all remaining characters are valid TFL symbols
        if Syntax.has_valid_symbols(line):

            # Check for matching parentheses
            if Syntax.has_balanced_parens(line):

                # Find the main logical operator
                if ('∧' or '∨' or '¬' or '→' or '↔') in line:
                    opIndex = Syntax.find_main_operator(line)
                    
                    # Grab the substrings around the main operator
                    left = line[0:opIndex]
                    right = line[opIndex+1:len(line)]

                    # There should be values on both sides unless the operator is ¬
                    if not (line[opIndex] == '¬'):
                        if left == '':
                            return False
                        if right == '':
                            return False

                    # Determine that both substrings are valid TFL sentences (recursion)
                    leftIsValid = Syntax.is_valid_TFL(left)
                    rightIsValid = Syntax.is_valid_TFL(right)
                    
                    if not (leftIsValid and rightIsValid):
                        return False

            else:
                return False
        
        else:
            return False

        # If we reached this line, everything checks out
        return True



    @staticmethod
    def remove_justification(str):
        """
        Removes the justification from the line, if present
        """

        line = str
        char = '#'
        if char in line:
            x = 0
            for char in line:
                if char == '#':
                    line = line[0:x]
                    break
                else:
                    x += 1

        return line

    @staticmethod
    def has_balanced_parens(str):
        """
        Determines if a string has balanced parentheses
        """
        OPEN_PARENS=['(', '[', '{']
        CLOSED_PARENS=[')', ']', '}']
        stack = []

        for char in str:
            if char in OPEN_PARENS:
                stack.append(char)
            elif char in CLOSED_PARENS:
                pos = CLOSED_PARENS.index(char)
                if ((len(stack) > 0) and 
                    (OPEN_PARENS[pos] == stack[len(stack)-1])):
                    stack.pop()
                else:
                    return False
        if len(stack)==0:
            return True
        else:
            return False

            
    @staticmethod
    def has_valid_symbols(str):
        """
        Verifies that all characters in a string are valid TFL symbols
        """
        # TODO: Replace ATOMIC with a more elegant regular expression
        ATOMIC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
            'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        CONNECTIVES = ['∧', '∨', '¬', '→', '↔']
        PARENS = ['(', '[', '{', ')', ']', '}']

        for char in str:
            if not ((char in ATOMIC) or (char in CONNECTIVES) or (char in PARENS)):
                return False

        return True

    @staticmethod
    def find_main_operator(str):
        """
        Returns the index of the main logical operator in a TFL sentence
        """
        CONNECTIVES = ['∧', '∨', '¬', '→', '↔']
        
        line = str
        opIndex = 0

        # Determine the depth of each char in the sentence
        depthArray = Syntax.set_depth_array(line)

        # Remove matching outermost parentheses
        if depthArray[0]==1:
            parensMatch = True
            index = 0
            # Depth drops to zero somewhere if outermost parentheses do not match
            for char in line[0:len(line)-1]:
                parensMatch = (parensMatch and depthArray[index]>0)
                index += 1
            # Strip the outermost parentheses, call function recursively
            # Add one to the result for the leading parenthesis that was removed
            if parensMatch:
                return (Syntax.find_main_operator(line[1:len(line)-1]) + 1)

        # Find the main operator
        for char in line:
            if ((char in CONNECTIVES) and (depthArray[opIndex]==0)):
                return opIndex
            else:
                opIndex += 1

        # If no operator found, return 0
        return 0

    @staticmethod
    def set_depth_array(str):
        """
        Returns an array containing the depth of each character in a TFL sentence
        """
        OPEN_PARENS=['(', '[', '{']
        CLOSED_PARENS=[')', ']', '}']

        depth = 0
        depthArray = []

        for char in str:
            if char in OPEN_PARENS:
                depth += 1
            elif char in CLOSED_PARENS:
                depth -= 1
            
            depthArray.append(depth)
        
        return depthArray
