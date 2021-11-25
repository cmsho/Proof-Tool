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

// Helper function to set multiple attributes at once
function setAttributes(el, attrs) {
    for(var key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}

// Call this at end of any function that changes the amount of forms
function update_form_count(){
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    let currentFormCount = document.getElementsByClassName("proofline-form").length
    totalNewForms.setAttribute('value', currentFormCount)
}

// Call this at the end of any function that changes the amount of forms
function update_form_ids() {
    const forms = document.getElementsByClassName("proofline-form")
    const fields = ['line_no', 'formula', 'rule', 'insert-btn', 'delete-btn']

    for (i = 0; i < forms.length; i++) {

        // Update the ID of each table row
        forms[i].setAttribute('id', `form-${i}`)

        // Update the ID of each input field (nested in <td>)
        var tds = forms[i].children
        for (x = 0; x < fields.length; x++) {
            // Input field is child of <td>
            var input = tds[x].children[0]
            input.setAttribute('name', `form-${i}-${fields[x]}`)
            input.setAttribute('id', `id_form-${i}-${fields[x]}`) 
        }
    }
}

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
        var newRow = create_empty_form()
        var tds = newRow.children

        for (x = 0; x < tds.length; x++) {
            var input = tds[x].children[0]
            // line_no
            if (x == 0) {
                input.setAttribute("value", i+1)
            }
            // formula
            if (x == 1) {
                input.setAttribute("value", `${premiseArray[i]}`)
            }
            // rule
            if (x == 2) {
                input.setAttribute("value", 'Premise')
            }
        }
        prooflineList.appendChild(newRow)
    }

    update_form_ids()
    update_form_count()
}