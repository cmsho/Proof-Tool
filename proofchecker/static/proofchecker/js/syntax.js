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