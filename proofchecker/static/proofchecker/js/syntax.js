/*
A Javascript equivalent to the current Syntax Python file that valid_input.js utilizes to check if the user's input is valid
*/

const ATOMIC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];

const CONNECTIVES = ['∧', '∨', '¬', '→', '→', '↔','^', '&', 'v', '>', '->', '<->', '-', '~']
const PARENS = ['(', '[', '{', ')', ']', '}'];
const OPEN_PARENS=['(', '[', '{'];
const CLOSED_PARENS=[')', ']', '}'];
const DELIMITERS = [',', ' '];

function isValidTFL(string) {

    /*
    Determine if a line of text represents a valid TFL statement
    Lines in a `prooftext` contain a justification after the '#' symbol
    If the line contains a justification, remove it
    */

    let line = "";
    line = string;
    if(line.includes('#'))
    {
        removeJustification(line);
    }
    
    //Strip all whitespace from the line
    line.replace(/\s+/g, '');

    //Verify all remaining characters are valid TFL symbols
    if(hasValidSymbols(line))
    {
        //Check for matching parentheses
        if(hasBalancedParens(line))
        {
            //Determine the depth of each char in the line
            let depthArray = setDepthArray(line);

            // Remove matching outermost parentheses
            if(depthArray[0] == 1)
            {
                let parenthesesMatch = true;
                let index = 0;

                //Depth drops to zero somewhere if outermost parentheses do not match
                for(var i = 0; i < line.length-1; i++)
                {
                    parenthesesMatch = parenthesesMatch && (depthArray[index] > 0);
                    index++;
                }

                //Strip the outermost parentheses, call function recursively
                //Add one to the result for the leading parenthesis that was removed
                if(parenthesesMatch)
                {
                    return isValidTFL(line.substring(1, line.length-1));
                }

                //Find the main logical operator
                if (line.includes('∧') || line.includes('∨') || line.includes('¬') || line.includes('→') || line.includes('↔'))
                {
                    let operatorIndex = findMainOperator(line);

                    //Grab the substrings around the main operator
                    let left = line.substring(0, operatorIndex);
                    let right = line.substring(operatorIndex+1, line.length);

                    //There should be values on both sides unless the operator is ¬
                    if(line.charAt(operatorIndex) != '¬')
                    {
                        if(left == '')
                        {
                            return "The left side of the main logical operator (" + line.charAt(operatorIndex) + ") is empty!";
                            //return false;
                        }
                        if(right == '')
                        {
                            return "The right side of the main logical operator (" + line.charAt(operatorIndex) + ") is empty!";
                            //return false;
                        }
                    }

                    //Determine that both substrings are valid TFL sentences (recursion)
                    let leftIsValid = isValidTFL(left);
                    let rightIsValid = isValidTFL(right);

                    if(!(leftIsValid && rightIsValid))
                    {                       
                        let substringError = "";

                        if(!leftIsValid)
                        {
                            substringError = substringError + "The left substring of the main operator (" + line.charAt(operatorIndex) + ") is invalid! ";
                        }
                               
                        if(!rightIsValid)
                        {
                            substringError = substringError + "The right substring of the main operator (" + line.charAt(operatorIndex) + ") is invalid!";
                        }
                     
                        
                         
                        return substringError;
                    }
                }
            }    
        }            
        else{
            return "This statement does not have balanced parantheses." ;
        }
    }
    else{
        return "This statement has at least one invalid TFL symbol." ;
    }

    //If we reached this line, everything checks out

    return "This is a valid TFL statement.";

}

function removeJustification(string){
    //Removes the justification from the line, if present
    let line = "";
    line = string;

    let char = '#';
    if(line.includes(char))
    {
        let endIndex = line.indexOf(char);
        line = line.substring(0, endIndex);
    }

    return line;

}

function hasBalancedParens(string){
    //Determines if a string has balanced parentheses
    let stack = [];
    let line = "";
    line = string;

    for(var i = 0; i < line.length; i++)
    {
        if(OPEN_PARENS.includes(line.charAt(i)))
        {
            stack.push(line.charAt(i));
        }
        else if(CLOSED_PARENS.includes(line.charAt(i)))
        {
            let position = CLOSED_PARENS.indexOf(line.charAt(i));
            if(stack.length > 0 && OPEN_PARENS[position] == stack[stack.length - 1])
            {
                stack.pop();
            }
            else{
                return false;
            }
        }
    }

    if(stack.length == 0)
    {
        return true;
    }

    return false;

}

function hasValidSymbols(string){

    let line = "";
    line = string;

    //Verifies that all characters in a string are valid TFL symbols
    for(var i = 0; i < line.length; i++)
    {
        if(!(ATOMIC.includes(line.charAt(i)) || CONNECTIVES.includes(line.charAt(i)) || PARENS.includes(line.charAt(i)) || DELIMITERS.includes(line.charAt(i))))
        {
            return false;
        }
    }

    return true;

}

function findMainOperator(string){

    //Returns the index of the main logical operator in a TFL sentence
    let line = "";
    line = string;

    let operatorIndex = 0;

    //Determine the depth of each char in the sentence
    let depthArray = setDepthArray(line);

    //Remove matching outermost parentheses
    if(depthArray[0] == 1)
    {
        let parenthesesMatch = true;
        let index = 0;

        //Depth drops to zero somewhere if outermost parentheses do not match
        for(var i = 0; i < line.length-1; i++)
        {
            parenthesesMatch = (parenthesesMatch && depthArray[index] > 0);
            index++;
        }

        //Strip the outermost parentheses, call function recursively
        //Add one to the result for the leading parenthesis that was removed
        if(parenthesesMatch)
        {
            line = line.substring(1, line.length-1);
            return findMainOperator(line) + 1;
        }

    }

    //Find the main operator
    for(var i = 0; i < line.length; i++)
    {
        if(CONNECTIVES.includes(line.charAt(i)) && depthArray[operatorIndex] == 0)
        {
            return operatorIndex;
        }
        else{
            operatorIndex++;
        }

    }

    //If no operator found, return 0
    return 0;        


}

function setDepthArray(string){

    //Returns an array containing the depth of each character in a TFL sentence

    let depth = 0;
    let depthArray = [];

    let line = "";
    line = string;

    for(var i = 0; i < line.length; i++)
    {
        if(OPEN_PARENS.includes(line.charAt(i)))
        {
            depth++;
        }
        else if(CLOSED_PARENS.includes(line.charAt(i)))
        {
            depth--;
        }

        depthArray.push(depth);
    }

    return depthArray;
}

function test_remove_justification_with_just()
{
    //remove_justification() should return the substring before the '#'
    let str = 'A∧B #∧I, 1,2';
    let str2 = removeJustification(str);
    //assertEqual(str2, 'A∧B ')
    if(str2 == 'A∧B ')
    {
        alert("Test 1 Success");
    }
    else
    {
        alert("Test 1 Failure");
    }
}

function test_remove_justification_without_just(){

    //remove_justification should return the same string if there is no '#'
    let str = '(A∧B)∨C';
    let str2 = removeJustification(str);
    //self.assertEqual(str2, '(A∧B)∨C')
    if(str2 == '(A∧B)∨C')
    {
        alert("Test 2 Success");
    }
    else
    {
        alert("Test 2 Failure");
    }
}

function test_has_valid_symbols_with_valid_symbols()
{
    //has_valid_symbols() should return True if all characters in the string are valid TFL symbols

    let str = '(A∧B)∨C';
    //self.assertIs(Syntax.has_valid_symbols(str), True)

    if(hasValidSymbols(str))
    {
        alert("Test 3 Success");
    }
    else
    {
        alert("Test 3 Failure");
    }
}

function test_has_valid_symbols_with_invalid_symbols(){

    //has_valid_symbols should return False if one or more characters in the string are not valid TFL symbols
    let str = 'A>B=C';
    //self.assertIs(Syntax.has_valid_symbols(str), False)
    if(!hasValidSymbols(str))
    {
        alert("Test 4 Success");
    }
    else
    {
        alert("Test 4 Failure");
    }
}

function test_has_balanced_parens_with_balanced_parens(){

    //has_balanced_parens should return True if all parentheses in the string are balanced and properly matching

    let str = '{[]{()}}';
    //self.assertIs(Syntax.has_balanced_parens(str), True)
    if(hasBalancedParens(str))
    {
        alert("Test 5 Success");
    }
    else
    {
        alert("Test 5 Failure");
    }
}

function test_has_balanced_parens_with_unbalanced_parens(){
    
    //"""has_balanced_parens should return False if parentheses in the string are unbalanced or not properly matching

    let str = '[{}{})(]'
    let str2 = '((()'
    let str3 = '(]'
    //self.assertIs(Syntax.has_balanced_parens(str), False)
    //self.assertIs(Syntax.has_balanced_parens(str2), False)
    //self.assertIs(Syntax.has_balanced_parens(str3), False)
    if(!hasBalancedParens(str) && !hasBalancedParens(str2) && !hasBalancedParens(str3))
    {
        alert("Test 6 success");
    }
    else
    {
        alert("Test 6 failure");
    }
}

function test_set_depth_array(){
    let str = '(A∧B)∨C';
    let str2 = '[(A∧B)∨C]';
    let depth_array = setDepthArray(str);
    let depth_array_2 = setDepthArray(str2);
    let a1 = [1, 1, 1, 1, 0, 0, 0]; 
    let a2 = [1, 2, 2, 2, 2, 1, 1, 1, 0];
    //self.assertEqual(depth_array, [1, 1, 1, 1, 0, 0, 0])
    //self.assertEqual(depth_array_2, [1, 2, 2, 2, 2, 1, 1, 1, 0])
    if(JSON.stringify(depth_array) == JSON.stringify(a1) && JSON.stringify(depth_array_2) == JSON.stringify(a2))
    {
        alert("Test 7 succcess");
    }
    else
    {
        alert("Test 7 failure");
    }

}

function test_find_main_operator_without_outer_parens1(){

    //find_main_operator should return the main logical operator of a TFL statement

    let str = '(A∧B)∨C'
    //self.assertEqual(Syntax.find_main_operator(str), 5)
    if(findMainOperator(str) == 5)
    {
        alert("Test 8 success");
    }
    else
    {
        alert("Test 8 failure");
    }
}

function test_find_main_operator_without_outer_parens2()
{
    // find_main_operator should return the main logical operator of a TFL statement
    let str = '[(A∧B)∨C]';
    //self.assertEqual(Syntax.find_main_operator(str), 6)
    if(findMainOperator(str) == 6)
    {
        alert("Test 9 success");
    }
    else
    {
        alert("Test 9 failure");
    }
}

function test_is_valid_TFL_with_atomic_sentence()
{
    //is_valid_TFL should return true if provided an atomic sentence
    let str1 = 'A';
    let str2 = 'Z';
    //self.assertIs(Syntax.is_valid_TFL(str1), True)
    //self.assertIs(Syntax.is_valid_TFL(str2), True)

    if(isValidTFL(str1) && isValidTFL(str2))
    {
        alert("Test 10 success");
    }
    else
    {
        alert("Test 10 failure");
    }
}

function test_is_valid_TFL_with_one_operator(){

    //is_valid_TFL should return true if provided a well-formed formula (WFF) with one operator
    let str1 = 'A∧B';
    let str2 = '(C∨D)';
    let str3 = '¬E';
    let str4 = '{X→Y}';
    let str5 = 'A↔Z';
    //self.assertIs(Syntax.is_valid_TFL(str1), True)
    //self.assertIs(Syntax.is_valid_TFL(str2), True)
    //self.assertIs(Syntax.is_valid_TFL(str3), True)
    //self.assertIs(Syntax.is_valid_TFL(str4), True)
    //self.assertIs(Syntax.is_valid_TFL(str5), True)
	
    if(isValidTFL(str1) == "This is a valid TFL statement." && isValidTFL(str2) == "This is a valid TFL statement." && isValidTFL(str3) == "This is a valid TFL statement." && isValidTFL(str4) == "This is a valid TFL statement." && isValidTFL(str5) == "This is a valid TFL statement.")
    {
        alert("Test 11 success");
    }
    else
    {
        alert("Test 11 failure");
    }
	
}

function test_is_valid_TFL_with_multiple_operators(){
    //is_valid_TFL should return true if provided a WFF with multiple operators

    let str1 = '(A∧B)∨C'
    let str2 = '(A∧B)∨[(¬C→D)∧(A↔Z)]'
    //self.assertIs(Syntax.is_valid_TFL(str1), True)
    //self.assertIs(Syntax.is_valid_TFL(str2), True)
    if(isValidTFL(str1) == "This is a valid TFL statement." && isValidTFL(str2) == "This is a valid TFL statement.")
    {
        alert("Test 12 success");
    }
    else
    {
        alert("Test 12 failure");
    }


}

function test_is_valid_TFL_with_invalid_input()
{
    //is_valid_TFL should return false if provided with a string that does not conform to TFL sentence rules
    let invalid_symbols = 'A+Z';
    let unbalanced_parens = '[A∧B)]';
    //self.assertIs(Syntax.is_valid_TFL(invalid_symbols), False)
    //self.assertIs(Syntax.is_valid_TFL(unbalanced_parens), False)
    if(isValidTFL(invalid_symbols) != "This is a valid TFL statement." && isValidTFL(unbalanced_parens) != "This is a valid TFL statement.")
    {
        alert("Test 13 success");
    }
    else
    {
        alert("Test 13 failure");
    }
}

function test_valid_symbols_with_comma_expression(sting)
{
    //An input string that delimits clauses with commmas should be accepted
    let str = 'AvB,A→B,B→C';

    if(hasValidSymbols(str))
    {
        alert("Test 14 success");
    }
    else
    {
        alert("Test 14 failure");
    }

}

function printTest()
{
    alert("Test print");
}