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
    for (var key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}

// Call this at end of any function that changes the amount of forms
function update_form_count() {
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    let currentFormCount = document.getElementsByClassName("proofline-form").length
    totalNewForms.setAttribute('value', currentFormCount)
}

// Call this at the end of any function that changes the amount of forms
function update_form_ids() {
    const forms = document.getElementsByClassName("proofline-form")
    const fields = ['line_no', 'formula', 'rule', 'insert-btn', 'create-subproof-btn', 'conclude-subproof-btn', 'delete-btn']

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

function get_total_forms_count_in_manager() {
    return parseInt(document.getElementById('id_proofline_set-TOTAL_FORMS').value)
}

function set_total_forms_count_in_manager(value) {
    document.getElementById('id_proofline_set-TOTAL_FORMS').setAttribute('value', value)
}

function create_empty_form() {
    const emptyFormElement = document.getElementById("empty-form").cloneNode(true)
    emptyFormElement.setAttribute("class", "proofline-form")
    return emptyFormElement
}

function get_form_id(obj) {
    return parseInt(obj.id.replace(/[^0-9]/g, ""))
}

// Inserts form below current line
function insert_form(obj) {
    insert_form_helper(get_form_id(obj) + 1)

    // function by thomas to insert a new row at the current level
    insert_row_current_level(get_form_id(obj) + 1)

}

function insert_form_helper(index) {

    const emptyFormElement = create_empty_form()
    emptyFormElement.setAttribute("id", `form-${index}`)
    const regex = new RegExp('__prefix__', 'g')
    emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, index)

    const proof_tbody = document.getElementById('proofline-list')
    const proof_table_row = document.getElementById('form-' + (index - 1))
    if (proof_table_row != null) {
        proof_table_row.after(emptyFormElement)
    } else {
        proof_tbody.append(emptyFormElement)
    }

    update_form_ids()
    update_form_count()
}


// function by thomas to insert a new row at the current level
function insert_row_current_level(index) {

    // since the new row is already inserted via the insert_form_helper this function is for assigning the correct row number


    // Get the new row
    var new_row = document.getElementById('form-' + (index))
    var new_row_number = new_row.children[0].children[0].value


    // retrieve the row where the button was clicked
    const row_number_of_clicked_button = document.getElementById('form-' + (index - 1)).children[0].children[0].value

    console.log(row_number_of_clicked_button)

    // Split the row number of clicked button value
    var row_number_of_clicked_button_list = row_number_of_clicked_button.split('.')

    // Get the prefix of the row number of button clicked
    var prefix_value_list = row_number_of_clicked_button_list.slice(0, -1)

    // If it has no subproof numbering then add one to the previous row number
    if (prefix_value_list.length == 0) {
        var prefix_value_string = prefix_value_list.join('.')
        new_row_number = `${Number(row_number_of_clicked_button) + 1}`
        new_row.children[0].children[0].value = new_row_number
    }
    // if it has subproof number then take the last number and add one to it
    else {
        var prefix_value_string = prefix_value_list.join('.')
        var last_value = row_number_of_clicked_button_list.at(-1)
        new_row_number = `${prefix_value_string}.${Number(last_value) + 1}`
        new_row.children[0].children[0].value = new_row_number
    }

    console.log("new_row_number")
    console.log(new_row_number)

    // Set the starting point for the renumbering
    var direction = 1;
    var starting_point = index + 1

    renumber_rows(direction, starting_point, prefix_value_list)
}

function renumber_rows(direction, starting_point, prefix_value_list) {

    // Forms that you'll iterate over
    const forms = document.getElementsByClassName("proofline-form")
    console.log(forms.length)
    var number_of_forms = forms.length

    // Get the prefix value string
    var index_of_changing_element = prefix_value_list.length
    var prefix_values_string = prefix_value_list.join('.')

    // Set the counter and the stopping point specific row numbers are renumbered
    var starting_form = (direction == 1) ? starting_point : number_of_forms - 1
    var stopping_point = (direction == 1) ? number_of_forms : starting_point - 1

    for (var current_form = starting_form; current_form != stopping_point; current_form += direction) {
        console.log(forms[current_form])

        // // Get the current form's row number
        var current_row_number = forms[current_form].children[0].children[0].value
        var current_row_number_list = current_row_number.split('.')

        if (current_row_number.startsWith(prefix_values_string)) {
            current_row_number_list[index_of_changing_element] = Number(current_row_number_list[index_of_changing_element]) + direction
            var new_row_number = current_row_number_list.join('.')

            forms[current_form].children[0].children[0].value = new_row_number
        }

    }

    return
}



// Adds new form at end of table
function add_form(event) {
    if (event) {
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

    // Added by Thomas Below
    console.log(emptyFormElement.children[0])
    emptyFormElement.children[0].children[0].setAttribute("value", currentFormCount + 1)
    // emptyFormElement.children[0].children[0].setAttribute("readonly", true)
    // Added by Thomas Above
    formCopyTarget.append(emptyFormElement)
    update_form_count()
}


function delete_form(obj) {

    var index = get_form_id(obj)
    const forms = document.getElementsByClassName("proofline-form")

    // retrieve the row where the button was clicked
    const row_number_of_clicked_button = document.getElementById('form-' + (index)).children[0].children[0].value

    console.log(row_number_of_clicked_button)

    // Split the row number of clicked button value
    var row_number_of_clicked_button_list = row_number_of_clicked_button.split('.')
    var prefix_value_list = row_number_of_clicked_button_list.slice(0, -1)
    var final_element_of_clicked_button_row = row_number_of_clicked_button_list.slice(-1)
    var prefix_value_string = prefix_value_list.join('.')


    var prefix_next_row_value_string = ""
    // if we're not deleting the last form check to see if we're deleting a sub proof
    if (index !== forms.length - 1) {
        var next_row_number = document.getElementById('form-' + (index + 1)).children[0].children[0].value
        console.log(next_row_number)
        var next_row_number_list = next_row_number.split('.')
        var prefix_of_next_row_list = next_row_number_list.slice(0, -1)
        var prefix_next_row_value_string = prefix_of_next_row_list.join('.')
    }



    var id = get_form_id(obj)
    const form_to_delete = document.getElementById("form-" + id)
    form_to_delete.remove()

    update_form_count()
    update_form_ids()

    // Set the starting point for the renumbering
    var direction = -1;
    var starting_point = index

    renumber_rows(direction, starting_point, prefix_value_list)

    // If we have deleted a sub proof then we need to update the numbers after
    if (final_element_of_clicked_button_row == "1" & !prefix_next_row_value_string.startsWith(prefix_value_string)) {

        if (prefix_value_list.length == prefix_of_next_row_list.length) {
            prefix_of_next_row_list.pop()
        }
        renumber_rows(direction, starting_point, prefix_of_next_row_list)
    }

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
                input.setAttribute("readonly", true)
                input.setAttribute("value", i + 1)
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