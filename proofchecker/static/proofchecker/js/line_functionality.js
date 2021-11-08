var headers = new Array();
headers = ['#', 'Expression', 'Justification', '', '', '']


function replaceCharacter(ev) {

    console.log(ev);

    if (ev.id == "premise" || ev.id == "conclusion") {
        var name = ev.id;
    } else {
        console.log(ev.path[0].id);
        var name = ev.path[0].id;
    }

    console.log(document.getElementById(name));
    let txt = document.getElementById(name).value;
    console.log(txt);

    txt = txt.replace("\\and", "∧");
    txt = txt.replace("\\or", "∨");
    txt = txt.replace("\\implies", "→");
    txt = txt.replace("\\not", "¬");
    txt = txt.replace("\\iff", "↔");
    txt = txt.replace("\\contradiction", "⊥");
    document.getElementById(name).value = txt;

}

function createNewRow(oButton, tr) {

    for (var cellCount = 0; cellCount < headers.length; cellCount++) {
        var td = document.createElement('td');
        td = tr.insertCell(cellCount);

        // If this is the first column add number
        if (cellCount == 0) {
            td.setAttribute('id', 'rowNumber');
            td.setAttribute('value', tr.rowIndex);
            td.innerHTML = tr.rowIndex;

        }

        // If this is the second column create input for expression
        if (cellCount == 1) {
            var inputField = document.createElement('input');

            var inputId = `expression-${tr.rowIndex}`;

            inputField.setAttribute('id', inputId);
            inputField.setAttribute('type', 'text');
            inputField.setAttribute('value', '');
            inputField.setAttribute("contenteditable", "true")
            inputField.addEventListener("input", replaceCharacter);
            td.appendChild(inputField);
        }

        // If this is the third column create input for justification
        if (cellCount == 2) {
            var inputField = document.createElement('input');

            var inputId = `justification-${tr.rowIndex}`;

            inputField.setAttribute('id', inputId);
            inputField.setAttribute('type', 'text');
            inputField.setAttribute('value', '');
            inputField.setAttribute("contenteditable", "true")
            inputField.addEventListener("input", replaceCharacter);
            td.appendChild(inputField);
        }

        // If this is the fourth column create button for adding 
        if (cellCount == 3) {
            var button = document.createElement('input');
            button.setAttribute('type', 'button');
            button.setAttribute('value', 'Insert New Row');
            button.setAttribute('onclick', 'insertNewRow(this)');
            td.appendChild(button);
        }
        // If this is the fifth column create button for adding sub
        if (cellCount == 4) {
            var button = document.createElement('input');
            button.setAttribute('type', 'button');
            button.setAttribute('value', 'Insert Sub Row');
            button.setAttribute('onclick', 'insertNewSubRow(this)');
            td.appendChild(button);
        }
        // If this is the six column create button for deleting
        if (cellCount == 5) {
            var button = document.createElement('input');
            button.setAttribute('type', 'button');
            button.setAttribute('value', 'Remove');
            button.setAttribute('onclick', 'removeRow(this)');
            td.appendChild(button);
        }

    }
    return tr;
}



function createTable(ev) {
    console.log(ev);


    var emptyTable = document.createElement('table');
    emptyTable.setAttribute('id', 'emptyTable');

    var tr = emptyTable.insertRow(-1);

    for (var headerCount = 0; headerCount < headers.length; headerCount++) {
        var th = document.createElement('th');
        th.innerHTML = headers[headerCount];
        tr.appendChild(th);
    }

    var div = document.getElementById('cont');
    div.appendChild(emptyTable);

    // console.log(document.getElementById('premise').value);
    var premise = document.getElementById('premise').value
    // console.log(document.getElementById('conclusion').value);
    var conclusion = document.getElementById('conclusion').value;

    var problem = `${premise} ∴ ${conclusion}`;

    document.getElementById("problem").innerHTML = problem;

    // Delimit the premise based on 
    var premises = premise.split(",").map(item => item.trim());

    // Iterate over the premises and create a new row for each
    var rowCount = 1;
    for (let premiseCount = 0; premiseCount < premises.length; premiseCount++) {
        appendNewRow();
        emptyTable.childNodes[0].childNodes[rowCount].childNodes[1].innerText = premises[premiseCount];
        emptyTable.childNodes[0].childNodes[rowCount].childNodes[2].innerText = "Premise";
        emptyTable.childNodes[0].childNodes[rowCount].childNodes[5].innerText = '';
        rowCount++;
    }
    return false;
}

function appendNewRow(oButton) {
    var emptyTable = document.getElementById('emptyTable');
    var rowCount = emptyTable.rows.length;
    var tr = emptyTable.insertRow(rowCount);
    createNewRow(oButton, tr);
}


// function to insert a row below current row
function insertNewRow(oButton) {
    const myList = oButton.parentNode.parentNode.parentNode;
    const myItem = oButton.parentNode.parentNode;
    var tr = document.createElement('tr');
    tr = createNewRow(oButton, tr);
    myList.insertBefore(tr, myItem.nextSibling);
    renumberRows();
}

function renumberRows() {
    var myTable = document.getElementById('emptyTable');
    var values = new Array();

    // console.log(myTable.rows.length);
    var rowNumberCounter = 2;

    for (var row = 2; row < myTable.rows.length; row++) {

        for (var cellCount = 0; cellCount < myTable.rows[row].cells.length; cellCount++) {
            var element = myTable.rows.item(row).cells[cellCount];

            // Update the row number
            if (cellCount == 0) {
                // console.log(element.innerText);
                element.innerText = rowNumberCounter;
            }

            // Update the expression id
            if (cellCount == 1) {
                // console.log(element.childNodes[0].id);
                element.childNodes[0].id = `expression-${rowNumberCounter}`;
                // console.log(element.childNodes[0].id);
            }

            // Update the justification id
            if (cellCount == 2) {
                element.childNodes[0].id = `justification-${rowNumberCounter}`;
            }
        }
        rowNumberCounter++;
    }
}


// function to insert a new row for a sub proof
function insertNewSubRow(oButton) {
    console.log("Add functionality to insert sub row")
}

// function to delete a row.
function removeRow(oButton) {
    var emptyTable = document.getElementById('emptyTable');
    emptyTable.deleteRow(oButton.parentNode.parentNode.rowIndex);
    renumberRows();
}

function submit() {

    var myTable = document.getElementById('emptyTable');
    var values = new Array();

    var proofObject = {};

    proofObject["proof"] = {};


    var premise = document.getElementById('premise').value
    var premises = premise.split(",").map(item => item.trim());
    var conclusion = document.getElementById('conclusion').value;



    var proof = proofObject["proof"];
    proof["premises"] = premises;
    proof["conclusion"] = conclusion;
    proof["lines"] = [];

    for (var row = 1; row < myTable.rows.length; row++) {
        var proofLine = {};
        for (var cellCount = 0; cellCount < myTable.rows[row].cells.length; cellCount++) {
            var element = myTable.rows.item(row).cells[cellCount];
            console.log(element);

            if (cellCount == 0) {
                values.push(element.innerText);
                proofLine["line_no"] = element.innerText;
            } else if (cellCount == 1) {
                values.push(element.childNodes[0].value ? element.childNodes[0].value : element.innerText)
                proofLine["expression"] = element.childNodes[0].value ? element.childNodes[0].value : element.innerText;
            } else if (cellCount == 2) {
                values.push(element.childNodes[0].value ? element.childNodes[0].value : element.innerText)
                proofLine["rule"] = element.childNodes[0].value ? element.childNodes[0].value : element.innerText;
            }
        }
        proof["lines"].push(proofLine);
    }

    console.log(proofObject);

    var jsonProofObject = JSON.stringify(proofObject);
    console.log(jsonProofObject);

}
