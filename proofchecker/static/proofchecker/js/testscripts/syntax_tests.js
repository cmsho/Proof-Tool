QUnit.test("Remove Justification with Just Symbol Test", function( assert ) { 

      //removeJustification() should return the substring before the '#'
      let str = 'A∧B #∧I, 1,2';
      let str2 = removeJustification(str);
      assert.equal(str2, 'A∧B ', "The string is A∧B.");
});

QUnit.test("Remove Justification without Just Symbol Test", function( assert ) { 

      //removeJustification should return the same string if there is no '#'
      let str = '(A∧B)∨C';
      let str2 = removeJustification(str);
      assert.equal(str2, '(A∧B)∨C', "The string is (A∧B)∨C");
});

QUnit.test("Has Valid Symbols with Valid Symbols Test", function( assert ) { 

      //hasValidSymbols() should return True if all characters in the string are valid TFL symbols
      var value = "A->B"; 
      var result = hasValidSymbols(value);
      assert.true(result, "The expression is valid!");
});

QUnit.test("Has Valid Symbols without Valid Symbols Test", function( assert ) { 

      //hasValidSymbols() should return False if one or more characters in the string are not valid TFL symbols
      var value = "A>B=C"; 
      var result = hasValidSymbols(value);
      assert.false(result, "The expression is invalid!");
});