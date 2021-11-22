function replaceCharacter(ev) {
    // console.log(document.getElementById(ev.id));
    let txt = document.getElementById(ev.id).value;
    // console.log(txt);

    txt = txt.replace("\\and", "∧");
    txt = txt.replace("\\or", "∨");
    txt = txt.replace("\\implies", "→");
    txt = txt.replace("\\not", "¬");
    txt = txt.replace("\\iff", "↔");
    txt = txt.replace("\\contradiction", "⊥");
    document.getElementById(ev.id).value = txt;
}

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

function delete_form(button) {
    // Delete the row
    var id = button.id.replace(/[^0-9]/g, "")
    const form_to_delete = document.getElementById("form-" + id)
    form_to_delete.remove()

    // Update the row count
    const currentProofLineForms = document.getElementsByClassName("proofline-form")
    let currentFormCount = currentProofLineForms.length
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    totalNewForms.setAttribute('value', currentFormCount)

    // Update row IDs
    update_form_ids()
}

function update_form_ids() {
    const forms = document.getElementsByClassName("proofline-form")
    for (i = 0; i < forms.length; i++) {

        // Update the ID of each table row
        forms[i].setAttribute('id', `form-${i}`)

        // Update the ID of each input field (nested in <td>)
        var children = forms[i].children
        for (x = 0; x < children.length; x++) {

            // Input field is child of <td>
            var input = children[x].children[0]

            // Rename all input fields
            if (x == 0) {
                input.setAttribute('name', `form-${i}-line_no`)
                input.setAttribute('id', `id_form-${i}-line_no`)
            }
            if (x == 1) {
                input.setAttribute('name', `form-${i}-formula`)
                input.setAttribute('id', `id_form-${i}-formula`)
            }
            if (x == 2) {
                input.setAttribute('name', `form-${i}-rule`)
                input.setAttribute('id', `id_form-${i}-rule`)
            }
            if (x == 3) {
                input.setAttribute('id', `delete-btn-${i}`)
            }
        }
    }
}

// Helper function to set multiple attributes at once
function setAttributes(el, attrs) {
    for (var key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}


const beginProofBtn = document.getElementById("begin_proof")
beginProofBtn.addEventListener("click", begin_proof)

// Function to automatically populate premise and conclusion values
function begin_proof() {

    var premises = document.getElementById('id_premises').value
    console.log(premises)
    var conclusion = document.getElementById('id_conclusion').value
    console.log(conclusion)

    // Separate the premises
    var premiseArray = premises.split(",").map(item => item.trim())
    console.log(premiseArray)

    var prooflineList = document.getElementById('proof-line-list')

    for (i = 0; i < premiseArray.length; i++) {
        console.log(`Writing line ${i}...`)
        var premiseRow = document.createElement('tr')
        premiseRow.setAttribute('class', 'proofline-form')

        for (x = 0; x < 4; x++) {
            var td = document.createElement('td')
            var input = document.createElement('input')

            // ------------------------------------
            // Set attributes for the input field

            // line_no
            if (x == 0) {
                var attrs = {
                    "type": "text",
                    "maxlength": "100",
                    "onkeydown": "replaceCharacter(this)",
                    "value": (i + 1)
                }
                setAttributes(input, attrs)
            }

            // formula
            if (x == 1) {
                var attrs = {
                    "type": "text",
                    "maxlength": "255",
                    "onkeydown": "replaceCharacter(this)",
                    "value": `${premiseArray[i]}`
                }
                setAttributes(input, attrs)
            }

            // rule
            if (x == 2) {
                var attrs = {
                    "type": "text",
                    "maxlength": "255",
                    "onkeydown": "replaceCharacter(this)",
                    "value": "Premise"
                }
                setAttributes(input, attrs)
            }

            // delete button
            if (x == 3) {
                var attrs = {
                    "class": "delete-row btn btn-secondary",
                    "type": "button",
                    "value": "Delete Row",
                    "onclick": "delete_form(this)"
                }
                setAttributes(input, attrs)
            }

            // ------------------------------------

            // Add <input> in <td>, add <td> in <tr>
            td.appendChild(input)
            console.log(`TD: \n${td}`)
            premiseRow.appendChild(td)
            console.log(`Premise Row: \n${premiseRow}`)

        }

        // Add <tr> in <tbody>
        prooflineList.appendChild(premiseRow)

    }

    // Update row IDs
    update_form_ids()

    // Update the form count
    update_form_count()

    // hide the begin_proof button
    const beginProofBtn = document.getElementById("begin_proof");
    beginProofBtn.style.display = 'none';

}

function update_form_count() {
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    const currentProofLineForms = document.getElementsByClassName("proofline-form")
    let currentFormCount = currentProofLineForms.length
    totalNewForms.setAttribute('value', currentFormCount)
}