window.onload = function () {

    const addMoreBtn = document.getElementById("add-more")
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    const currentProofLineForms = document.getElementsByClassName("proofline-form")
    addMoreBtn.addEventListener("click", add_new_form)


    var headers = new Array();
    headers = ['#', 'Expression', 'Justification', '', '', '', '']
    const addRowButton = document.getElementById("add-table-row");
    addRowButton.addEventListener("click", appendNewRow);


    function add_new_form(event) {
        if (event) {
            event.preventDefault()
        }
        let currentFormCount = currentProofLineForms.length
        const formCopyTarget = document.getElementById("proof-line-list")
        const emptyFormElement = document.getElementById("empty-form").cloneNode(true)
        emptyFormElement.setAttribute("class", "proofline-form")
        emptyFormElement.setAttribute("id", `form-${currentFormCount}`)
        const regex = new RegExp('__prefix__', 'g')
        emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, currentFormCount)
        totalNewForms.setAttribute('value', currentFormCount + 1)
        formCopyTarget.append(emptyFormElement)
    }



    function createNewRow(event, tr) {



        for (var cellCount = 0; cellCount < headers.length; cellCount++) {
            var td = document.createElement('td');
            td = tr.insertCell(cellCount);


            // Create a clone of the form
            const emptyFormElement = document.getElementById("empty-form").cloneNode(true)
            // emptyFormElement.setAttribute("id", `form-${currentFormCount}`)
            const regex = new RegExp('__prefix__', 'g')
            // emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, currentFormCount)

            console.log(emptyFormElement);
            console.log(emptyFormElement.childNodes.item("id_form-__prefix__-rule"));
            // console.log(emptyFormElement.getElementById("id_form-__prefix__-rule"));

            // If this is the first column add number
            if (cellCount == 0) {

                td.setAttribute('id', 'rowNumber');
                td.setAttribute('value', tr.rowIndex);
                td.innerHTML = tr.rowIndex;
            }

            // If this is the second column create input for expression
            if (cellCount == 1) {
                // var inputField = document.createElement('input');

                // var inputId = `expression-${tr.rowIndex}`;

                // inputField.setAttribute('id', inputId);
                // inputField.setAttribute('type', 'text');
                // inputField.setAttribute('value', '');
                // inputField.setAttribute("contenteditable", "true")
                // inputField.addEventListener("input", replaceCharacter);
                // td.appendChild(inputField);
            }

            // If this is the third column create input for justification
            if (cellCount == 2) {
                // var inputField = document.createElement('input');

                // var inputId = `justification-${tr.rowIndex}`;

                // inputField.setAttribute('id', inputId);
                // inputField.setAttribute('type', 'text');
                // inputField.setAttribute('value', '');
                // inputField.setAttribute("contenteditable", "true")
                // inputField.addEventListener("input", replaceCharacter);
                // td.appendChild(inputField);
            }

            // If this is the fourth column create button for adding line in current position
            if (cellCount == 3) {
                // var button = document.createElement('input');
                // button.setAttribute('type', 'button');
                // button.setAttribute('value', 'Insert Row Current Level');
                // button.setAttribute('onclick', 'insertRowCurrentLevel(this)');
                // td.appendChild(button);
            }

            // If this is the fifth column create button for adding sub
            if (cellCount == 4) {
                // var button = document.createElement('input');
                // button.setAttribute('type', 'button');
                // button.setAttribute('value', 'Begin Subproof');
                // button.setAttribute('onclick', 'beginSubproof(this)');
                // td.appendChild(button);
            }
            // If this is the six column create button for deleting
            if (cellCount == 5) {
                // var button = document.createElement('input');
                // button.setAttribute('type', 'button');
                // button.setAttribute('value', 'Remove');
                // button.setAttribute('onclick', 'removeRow(this)');
                // td.appendChild(button);
            }

            if (cellCount == 6) {
                // var button = document.createElement('input');
                // button.setAttribute('type', 'button');
                // button.setAttribute('value', 'Conclude Subproof');
                // button.setAttribute('onclick', 'concludeSubproof(this)');
                // td.appendChild(button);
            }

        }


    }


    function appendNewRow(event) {
        if (event) {
            event.preventDefault()
        }
        var proofTable = document.getElementById("proof-table");
        console.log(proofTable);

        var rowCount = proofTable.rows.length;
        // var newRow = proofTable.insertRow(rowCount);

        // console.log(newRow);
        // createNewRow(event, newRow);

        var row = document.getElementById("to-clone");

        var emptyFormElement = row.cloneNode(true);
        // emptyFormElement.id = "NewID";
        emptyFormElement.setAttribute("class", "proofline-form")
        emptyFormElement.setAttribute("id", `form-${rowCount}`)
        const regex = new RegExp('__prefix__', 'g')
        emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, rowCount)
        totalNewForms.setAttribute('value', rowCount + 1)

        proofTable.appendChild(emptyFormElement);



        // const emptyFormElement = document.getElementById("empty-form").cloneNode(true);

        // proofTable.append(emptyFormElement);




        // var rowCount = emptyTable.rows.length;
        // var tr = emptyTable.insertRow(rowCount);
        // createNewRow(oButton, tr);


    }


}



// function appendNewRow(oButton) {
//     const emptyTable = document.getElementById('emptyTable');
//     var rowCount = emptyTable.rows.length;
//     var newRow = emptyTable.insertRow(rowCount);
//     createNewRow(oButton, newRow);

//     var previousRowNumber = emptyTable.rows.item(rowCount - 1).cells[0].innerHTML

//     var previousRowNumberList = previousRowNumber.split('.');
//     var newRowNumber = Number(previousRowNumberList[0]) + 1;
//     newRow.childNodes[0].innerHTML = newRowNumber;

//     newRow.childNodes[1].childNodes[0].id = `expression-${newRowNumber}`
//     newRow.childNodes[2].childNodes[0].id = `justification-${newRowNumber}`

// }



// var headers = new Array();
// headers = ['#', 'Expression', 'Justification', '', '', '', '']

// function createTable(ev) {
//     console.log(ev);


//     var emptyTable = document.createElement('table');
//     emptyTable.setAttribute('id', 'emptyTable');

//     var tr = emptyTable.insertRow(-1);

//     for (var headerCount = 0; headerCount < headers.length; headerCount++) {
//         var th = document.createElement('th');
//         th.innerHTML = headers[headerCount];
//         tr.appendChild(th);
//     }

//     var div = document.getElementById('cont');
//     div.appendChild(emptyTable);

//     // console.log(document.getElementById('premise').value);
//     var premise = document.getElementById('premise').value
//     // console.log(document.getElementById('conclusion').value);
//     var conclusion = document.getElementById('conclusion').value;

//     var problem = `${premise} ∴ ${conclusion}`;

//     document.getElementById("problem").innerHTML = problem;

//     // Delimit the premise based on 
//     var premises = premise.split(",").map(item => item.trim());

//     // Iterate over the premises and create a new row for each
//     var rowCount = 1;

//     for (let premiseCount = 0; premiseCount < premises.length; premiseCount++) {
//         addPremiseRows();
//         emptyTable.childNodes[0].childNodes[rowCount].childNodes[1].innerText = premises[premiseCount];
//         emptyTable.childNodes[0].childNodes[rowCount].childNodes[2].innerText = "Premise";
//         emptyTable.childNodes[0].childNodes[rowCount].childNodes[4].innerText = '';
//         emptyTable.childNodes[0].childNodes[rowCount].childNodes[5].innerText = '';
//         emptyTable.childNodes[0].childNodes[rowCount].childNodes[6].innerText = '';
//         rowCount++;
//     }
//     return false;
// }