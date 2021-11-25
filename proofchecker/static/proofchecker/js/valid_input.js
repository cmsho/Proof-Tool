const premisesBox = document.getElementById('id_premises');
const conclusionBox = document.getElementById('id_conclusion');

premisesBox.addEventListener("focusout", isValidPremiseInput);
conclusionBox.addEventListener("focusout", isValidConclusionInput);


function isValidPremiseInput()
{
    let premiseInput = "";
    premiseInput = premisesBox.value;
    if(premiseInput != "" && premiseInput.includes('@'))
    {
        invalidInputMessage();
    }
}

function isValidConclusionInput()
{
    let conclusionInput = "";
    conclusionInput = conclusionBox.value;

    if(conclusionInput != "" && conclusionInput.includes('@'))
    {
        invalidInputMessage();
    }
}


function invalidInputMessage(){
    alert("The input is invalid");
}