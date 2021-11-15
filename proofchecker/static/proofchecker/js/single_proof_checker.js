window.onload = function () {
    const addMoreBtn = document.getElementById("add-more")
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    const currentProofLineForms = document.getElementsByClassName("proofline-form")
    addMoreBtn.addEventListener("click", add_new_form)
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
}



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