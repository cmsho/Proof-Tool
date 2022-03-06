const premisesBox = document.getElementById('id_premises');
const conclusionBox = document.getElementById('id_conclusion');

premisesBox.addEventListener("focusout", isValidPremiseInput);
conclusionBox.addEventListener("focusout", isValidConclusionInput);

function applyTest(elementID)
{
    let proofBox = document.getElementById(elementID);
    proofBox.addEventListener("onmouseover", makeGreen(elementID));
    proofBox.addEventListener("onmouseout", makeWhite(elementID));
}

function makeGreen(elementID)
{
    let proofBox = document.getElementById(elementID);
    proofBox.style.backgroundColor = "green";
}

function makeWhite(elementID)
{
    let proofBox = document.getElementById(elementID);
    proofBox.style.backgroundColor = "white";
}

function isValidPremiseInput()
{
    let premiseInput = "";
    premiseInput = premisesBox.value;
    if(premiseInput != "" && !isValidTFL(premiseInput).includes("This is a valid TFL statement."))
    {
        invalidPremiseInputMessage(isValidTFL(premiseInput));
    }
    else
    {
        clearPremiseErrorDiv();
    }
}

function isValidConclusionInput()
{
    let conclusionInput = "";
    conclusionInput = conclusionBox.value;

    if(conclusionInput != "" && !isValidTFL(conclusionInput).includes("This is a valid TFL statement."))
    {
        invalidConclusionInputMessage(isValidTFL(conclusionInput));
    }
    else
    {
        clearConclusionErrorDiv();
    }
}


function invalidPremiseInputMessage(string){

    let errorString = "";
    errorString = string;
    let premiseHeader = "Premise Error: ";

    let errorDiv = document.getElementById('valid-premise-div');

    errorDiv.innerHTML = premiseHeader.bold() + errorString;
    setPremiseTooltipError(errorString);
}


function invalidConclusionInputMessage(string){

    let errorString = "";
    errorString = string;
    let conclusionHeader = "Conclusion Error: ";

    let errorDiv = document.getElementById('valid-conclusion-div');

    errorDiv.innerHTML = conclusionHeader.bold() + errorString;
}

function clearPremiseErrorDiv()
{
    let errorDiv = document.getElementById('valid-premise-div');
    errorDiv.innerHTML = "";

}

function clearConclusionErrorDiv()
{
    let errorDiv = document.getElementById('valid-conclusion-div');
    errorDiv.innerHTML = "";
}