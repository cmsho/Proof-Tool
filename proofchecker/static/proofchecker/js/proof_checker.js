// Add event listeners to buttons
const addMoreBtn = document.getElementById("add-more")
addMoreBtn.addEventListener("click", add_form)

const beginProofBtn = document.getElementById("begin_proof")
beginProofBtn.addEventListener("click", begin_proof)


// Text replacement - replaces escape commands with symbols
function replaceCharacter(ev) {
    let txt = document.getElementById(ev.id).value;
    txt = txt.replace("\\and", "∧");
    txt = txt.replace("\\or", "∨");
    txt = txt.replace("\\implies", "→");
    txt = txt.replace("\\not", "¬");
    txt = txt.replace("\\iff", "↔");
    txt = txt.replace("\\contradiction", "⊥");
    document.getElementById(ev.id).value = txt;
}

<<<<<<< HEAD
const addMoreBtn = document.getElementById("add-more")
const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
const currentProofLineForms = document.getElementsByClassName("proofline-form")
addMoreBtn.addEventListener("click", add_new_form)

function add_new_form(event) {
    if (event) {
        event.preventDefault()
=======
// Helper function to set multiple attributes at once
function setAttributes(el, attrs) {
    for(var key in attrs) {
        el.setAttribute(key, attrs[key]);
>>>>>>> main
    }
}

<<<<<<< HEAD
function delete_form(button) {
    // Delete the row
    var id = button.id.replace(/[^0-9]/g, "")
    const form_to_delete = document.getElementById("form-" + id)
    form_to_delete.remove()

    // Update the row count
    const currentProofLineForms = document.getElementsByClassName("proofline-form")
    let currentFormCount = currentProofLineForms.length
=======
// Call this at end of any function that changes the amount of forms
function update_form_count(){
>>>>>>> main
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    let currentFormCount = document.getElementsByClassName("proofline-form").length
    totalNewForms.setAttribute('value', currentFormCount)
}

// Call this at the end of any function that changes the amount of forms
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
<<<<<<< HEAD
            if (x == 3) {
=======
            if (x==3) {
                input.setAttribute('id', `insert-btn-${i}`)
            }
            if (x==4) {
>>>>>>> main
                input.setAttribute('id', `delete-btn-${i}`)
            }
        }
    }
}

<<<<<<< HEAD
// Helper function to set multiple attributes at once
function setAttributes(el, attrs) {
    for (var key in attrs) {
        el.setAttribute(key, attrs[key]);
=======
function get_total_forms_count() {
    return document.getElementsByClassName("proofline-form").length
}

function get_total_forms_count_in_manager(){
    return parseInt(document.getElementById('id_proofline_set-TOTAL_FORMS').value)
}

function set_total_forms_count_in_manager(value){
    document.getElementById('id_proofline_set-TOTAL_FORMS').setAttribute('value', value)
}

function create_empty_form() {
    const emptyFormElement = document.getElementById("empty-form").cloneNode(true)
    emptyFormElement.setAttribute("class", "proofline-form")
    return emptyFormElement
}

function get_form_id(obj){
    return parseInt(obj.id.replace(/[^0-9]/g, ""))
}

// Inserts form below current line
function insert_form(obj) {
    insert_form_helper(get_form_id(obj)+1)
}

function insert_form_helper(index) {

    const emptyFormElement = create_empty_form()
    emptyFormElement.setAttribute("id", `form-${index}`)
    const regex = new RegExp('__prefix__', 'g')
    emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, index)

    const proof_tbody = document.getElementById('proofline-list')
    const proof_table_row = document.getElementById('form-'+(index-1))
    if (proof_table_row != null){
        proof_table_row.after(emptyFormElement)
    } else {
        proof_tbody.append(emptyFormElement)
>>>>>>> main
    }

    update_form_ids()
    update_form_count()
}

// Adds new form at end of table
function add_form(event){
    if (event){
        event.preventDefault()
    }
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    const currentProofLineForms = document.getElementsByClassName("proofline-form")
    let currentFormCount = currentProofLineForms.length
    const formCopyTarget = document.getElementById("proofline-list")
    emptyFormElement = create_empty_form()
    emptyFormElement.setAttribute("id", `form-${currentFormCount}`)
    const regex = new RegExp('__prefix__', 'g')
    emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, currentFormCount)
    formCopyTarget.append(emptyFormElement)
    update_form_count()
}


function delete_form(obj){
    var id = get_form_id(obj)
    const form_to_delete = document.getElementById("form-" + id)
    form_to_delete.remove()

    update_form_count()
    update_form_ids()
}


// Automatically populate the premise values 
function begin_proof() {

    var premises = document.getElementById('id_premises').value
    var premiseArray = premises.split(",").map(item => item.trim())
    var prooflineList = document.getElementById('proofline-list')

    for (i = 0; i < premiseArray.length; i++) {
        var premiseRow = document.createElement('tr')
        premiseRow.setAttribute('class', 'proofline-form')

        for (x = 0; x < 5; x++) {
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
<<<<<<< HEAD

            // delete button
=======
    
            // insert button
>>>>>>> main
            if (x == 3) {
                var attrs = {
                    "class": "insert-row btn btn-secondary",
                    "type": "button",
                    "value": "Insert Row",
                    "onclick": "insert_form(this)"
                }
                setAttributes(input, attrs)
            }

            // delete button
            if (x == 4) {
                var attrs = {
                    "class": "delete-row btn btn-secondary",
                    "type": "button",
                    "value": "Delete Row",
                    "onclick": "delete_form(this)"
                }
                setAttributes(input, attrs)
            }
<<<<<<< HEAD

=======
>>>>>>> main
            // ------------------------------------

            // Add <input> in <td>, add <td> in <tr>
            td.appendChild(input)
            premiseRow.appendChild(td)
<<<<<<< HEAD
            console.log(`Premise Row: \n${premiseRow}`)

        }

=======
        }
>>>>>>> main
        // Add <tr> in <tbody>
        prooflineList.appendChild(premiseRow)
    }

    update_form_ids()
    update_form_count()
<<<<<<< HEAD

    // hide the begin_proof button
    const beginProofBtn = document.getElementById("begin_proof");
    beginProofBtn.style.display = 'none';

}

function update_form_count() {
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    const currentProofLineForms = document.getElementsByClassName("proofline-form")
    let currentFormCount = currentProofLineForms.length
    totalNewForms.setAttribute('value', currentFormCount)
=======
>>>>>>> main
}