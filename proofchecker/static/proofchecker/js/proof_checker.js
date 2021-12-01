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

function create_subproof(obj) {
    insert_form_helper(get_form_id(obj) + 1)

    generate_new_subproof_row_number(get_form_id(obj) + 1)
}

function conclude_subproof(obj) {
    insert_form_helper(get_form_id(obj) + 1)

    insert_row_parent_level(get_form_id(obj) + 1)
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

    // hide_conclude_button()

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


function generate_new_subproof_row_number(index) {

    // Get the row that the button was clicked
    var row_number_of_clicked_button = document.getElementById('form-' + (index - 1)).children[0].children[0].value
    const original_row_number_of_clicked_button = row_number_of_clicked_button


    // Update row number of clicked button
    document.getElementById('form-' + (index - 1)).children[0].children[0].value = `${original_row_number_of_clicked_button}.1`

    // Update the row number of the new row
    document.getElementById('form-' + (index)).children[0].children[0].value = `${original_row_number_of_clicked_button}.2`

    // hide_conclude_button()
}


function insert_row_parent_level(index) {

    // Get the row being deleted
    var row_above_added = document.getElementById('form-' + (index - 1))
    var line_number_of_row_above_added = row_above_added.children[0].children[0].value

    // Get list of row being deleted
    var list_of_row_above_added = line_number_of_row_above_added.split('.')
    // Get the prefix of the row being deleted
    var prefix_of_row_above_added = list_of_row_above_added.slice(0, -1)
    // Get string of prefix of row being deleted
    var string_of_prefix_above_added = prefix_of_row_above_added.join('.')
    // Get the last value of the row being deleted
    var final_value_of_row_above_added = list_of_row_above_added.slice(-1)


    // Create the new row number
    var new_row_number = prefix_of_row_above_added
    // console.log(new_row_number)

    new_row_number[new_row_number.length - 1] = `${Number(new_row_number[new_row_number.length - 1]) + 1}`
    // console.log(new_row_number)
    document.getElementById('form-' + (index)).children[0].children[0].value = new_row_number.join('.')


    var direction = 1
    var starting_point = index + 1
    // var prefix_value_list = new_row_number

    var prefix_value_list = new_row_number.length > 1 ? new_row_number : []

    console.log("Prefix value")
    console.log(prefix_value_list)


    renumber_rows(direction, starting_point, prefix_value_list)


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
    if (currentFormCount > 0) {
        var previous_row_number = document.getElementById('form-' + (currentFormCount - 1)).children[0].children[0].value
        var new_row_number = `${Number(previous_row_number[0]) + 1}`
    } else {
        var new_row_number = '1'
    }
    emptyFormElement.children[0].children[0].setAttribute("value", new_row_number)
    // emptyFormElement.children[0].children[0].setAttribute("readonly", true)
    // Added by Thomas Above
    formCopyTarget.append(emptyFormElement)
    update_form_count()
}

function get_row(index) {

    var row_object = document.getElementById('form-' + (index))
    // Get line number of the row
    var line_number_of_row = row_object.children[0].children[0].value
    // Get list of number of row
    var list_of_line_number = line_number_of_row.split('.')
    // Get the prefix of the row 
    var prefix_of_row = list_of_line_number.slice(0, -1)
    // Get the string of the prefix
    var string_of_prefix = prefix_of_row.join('.')
    // Get the final value of row
    var final_value = list_of_line_number.slice(-1)

    var row = {
        // Get object of the row
        "row_object": row_object,
        // Get line number of the row
        "line_number_of_row": line_number_of_row,
        // Get list of number of row
        "list_of_line_number": list_of_line_number,
        // Get the prefix of the row 
        "prefix_of_row": prefix_of_row,
        // Get the string of the prefix
        "string_of_prefix": string_of_prefix,
        // Get the final value of row
        "final_value": final_value,
    }
    return row
}


function get_rows(obj) {

    // Get index of the row where the button was clicked
    var index = get_form_id(obj)
    var forms = document.getElementsByClassName("proofline-form")
    var index_of_last_row = forms.length - 1

    // Get row above where the button was clicked if it's not the first row
    if (index != 0) {
        // Get object of the row
        var row_above_button_click = document.getElementById('form-' + (index - 1))
        // Get line number of the row
        var line_number_of_row_above = row_above_button_click.children[0].children[0].value
        // Get list of number of the row
        var list_of_line_number_of_row_above = line_number_of_row_above.split('.')
        // Get the prefix of the row
        var prefix_of_row_above = list_of_line_number_of_row_above.slice(0, -1)
        // Get the string of the prefix of the row above 
        var string_of_prefix_above_row = prefix_of_row_above.join('.')
    }

    // Get row the button was clicked on
    // Get object of the row
    var row_of_button_click = document.getElementById('form-' + (index))
    // Get line number of the row
    var line_number_of_row = row_above_button_click.children[0].children[0].value
    // Get list of number of row
    var list_of_line_number = line_number_of_row.split('.')
    // Get the prefix of the row 
    var prefix_of_row = list_of_line_number.slice(0, -1)
    // Get the string of the prefix
    var string_of_prefix = prefix_of_row.join('.')
    // Get the final value of row
    var final_value = list_of_line_number.slice(-1)

    var string_of_prefix_below_row = ""
    // Get row after where the button was clicked
    if (index != index_of_last_row) {
        // Get object of the row
        var row_below_button_click = document.getElementById('form-' + (index + 1))
        // Get line number of the row
        var line_number_of_row_below = row_below_button_click.children[0].children[0].value
        // Get list of number of the row
        var list_of_line_number_of_row_below = line_number_of_row_below.split('.')
        // Get prefix of the row
        var prefix_of_row_below = list_of_line_number_of_row_below.slice(0, -1)
        // Get the string of the prefix of the row above 
        var string_of_prefix_below_row = prefix_of_row_below.join('.')
    }

}


function delete_form(obj) {
    var index = get_form_id(obj)
    var forms = document.getElementsByClassName("proofline-form")
    var index_of_last_row = forms.length - 1

    if (index != 0) {
        var above_row = get_row(index - 1)
    }
    var button_row = get_row(index)

    if (index != index_of_last_row) {
        var below_row = get_row(index + 1)
    }

    // Delete row
    const form_to_delete = document.getElementById("form-" + index)
    form_to_delete.remove()
    update_form_count()
    update_form_ids()

    // Set the direction of the renumbering to -1 to start from the end of the forms
    var direction = -1
    // Set the starting point of the renumbering to the index of the removed line
    var starting_point = index

    renumber_rows(direction, starting_point, button_row.prefix_of_row)

    // If a sub proof is being deleted
    if ((index != index_of_last_row) & (button_row.final_value == "1") & (button_row.list_of_line_number.length > 1)) {

        // How to handle when a parent sub proof is deleted
        if ((below_row.string_of_prefix.startsWith(above_row.string_of_prefix)) & (above_row.string_of_prefix.length >= 1)) {
            console.log("sub proof of sub proof")
            renumber_rows(direction, starting_point, above_row.list_of_line_number)
        }
        // How to handle all other cases
        else if (button_row.string_of_prefix != below_row.string_of_prefix) {
            console.log("Deleting subproof")
            renumber_rows(direction, starting_point, above_row.prefix_of_row)
        }
    }

}


// function delete_form_former(obj) {

//     // Get index of row being deleted and the index of the last row
//     var index = get_form_id(obj)
//     var forms = document.getElementsByClassName("proofline-form")
//     var index_of_last_row = forms.length - 1

//     // If not first row get the row before the one being deleted
//     if (index != 0) {
//         var row_above_deleted = document.getElementById('form-' + (index - 1))
//         var line_number_of_row_above_deleted = row_above_deleted.children[0].children[0].value
//         // Create list of row above deleted
//         var list_of_row_above_deleted = line_number_of_row_above_deleted.split('.')
//         // Get the prefix of the row above deleted
//         var prefix_of_row_above_deleted = list_of_row_above_deleted.slice(0, -1)
//         // Get string of the prefix of row above deleted
//         var string_of_prefix_above_deleted = prefix_of_row_above_deleted.join('.')
//     }

//     // Get the row being deleted
//     var row_being_deleted = document.getElementById('form-' + (index))
//     var line_number_of_row_being_deleted = row_being_deleted.children[0].children[0].value

//     // Get list of row being deleted
//     var list_of_row_being_deleted = line_number_of_row_being_deleted.split('.')
//     // Get the prefix of the row being deleted
//     var prefix_of_row_being_deleted = list_of_row_being_deleted.slice(0, -1)
//     // Get string of prefix of row being deleted
//     var string_of_prefix_being_deleted = prefix_of_row_being_deleted.join('.')
//     // Get the last value of the row being deleted
//     var final_value_of_row_being_deleted = list_of_row_being_deleted.slice(-1)


//     var string_of_prefix_below_deleted = ""
//     // If not last row get the row after the row being deleted
//     if (index != index_of_last_row) {
//         var row_below_deleted = document.getElementById('form-' + (index + 1))
//         var line_number_of_row_below_deleted = row_below_deleted.children[0].children[0].value

//         // Get list of row below deleted
//         var list_of_row_below_deleted = line_number_of_row_below_deleted.split('.')
//         // Get the prefix of the row below deleted
//         var prefix_of_row_below_deleted = list_of_row_below_deleted.slice(0, -1)
//         // Get the string of the prefix below deleted
//         var string_of_prefix_below_deleted = prefix_of_row_below_deleted.join('.')
//     }

//     // Delete row
//     const form_to_delete = document.getElementById("form-" + index)
//     form_to_delete.remove()
//     update_form_count()
//     update_form_ids()


//     // Set the direction of the renumbering to -1 to start from the end of the forms
//     var direction = -1
//     // Set the starting point of the renumbering to the index of the removed line
//     var starting_point = index

//     renumber_rows(direction, starting_point, prefix_of_row_being_deleted)

//     // If a sub proof is being deleted
//     if ((index != index_of_last_row) & (final_value_of_row_being_deleted == "1") & (list_of_row_being_deleted.length > 1)) {

//         // How to handle when a parent sub proof is deleted
//         if ((string_of_prefix_below_deleted.startsWith(string_of_prefix_above_deleted)) & (string_of_prefix_above_deleted.length >= 1)) {
//             console.log("sub proof of sub proof")
//             renumber_rows(direction, starting_point, list_of_row_above_deleted)
//         }
//         // How to handle all other cases
//         else if (string_of_prefix_being_deleted != string_of_prefix_below_deleted) {
//             console.log("Deleting subproof")
//             console.log(prefix_of_row_above_deleted)
//             renumber_rows(direction, starting_point, prefix_of_row_above_deleted)
//         }
//     }
// }


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

        // console.log("Current row")
        // console.log(current_row_number)
        // console.log(prefix_values_string)
        // console.log(["index", index_of_changing_element])

        if (current_row_number.startsWith(prefix_values_string)) {
            current_row_number_list[index_of_changing_element] = Number(current_row_number_list[index_of_changing_element]) + direction
            var new_row_number = current_row_number_list.join('.')

            forms[current_form].children[0].children[0].value = new_row_number
        }
    }

    // hide_conclude_button()
}


function hide_conclude_button() {
    // Forms that you'll iterate over
    const forms = document.getElementsByClassName("proofline-form")
    // console.log(forms.length)
    var number_of_forms = forms.length - 1

    for (var current_form = 0; current_form <= number_of_forms; current_form++) {
        console.log(["row", current_form])

        console.log(document.getElementById(`form-${current_form}`))

        document.getElementById(`form-${current_form}`).children[5].children[0].style.visibility = 'hidden'

        // console.log(forms[current_form].children[0].children[0].value)
        // console.log(forms[current_form])

        // if (current_form < number_of_forms) {

        //     var line_number_of_current_row = forms[current_form].children[0].children[0].value

        //     // Get list of row being deleted
        //     var list_of_current_row = line_number_of_current_row.split('.')
        //     // Get the prefix of the row being deleted
        //     var prefix_of_current_row = list_of_current_row.slice(0, -1)
        //     // Get string of prefix of row being deleted
        //     var string_of_prefix_current_row = prefix_of_current_row.join('.')
        //     // Get the last value of the row being deleted
        //     var final_value_of_current_row = list_of_current_row.slice(-1)




        //     var line_number_of_next_row = forms[current_form + 1].children[0].children[0].value

        //     // Get list of row below deleted
        //     var list_of_next_row = line_number_of_next_row.split('.')
        //     // Get the prefix of the row below deleted
        //     var prefix_of_next_row = list_of_next_row.slice(0, -1)
        //     // Get the string of the prefix below deleted
        //     var string_of_prefix_next_row = prefix_of_next_row.join('.')

        //     // console.log("row")
        //     // console.log(list_of_current_row, list_of_next_row)

        //     // console.log(prefix_of_current_row.join('.'))
        //     // console.log(prefix_of_next_row.join('.'))

        //     if (prefix_of_current_row.join('.') == prefix_of_next_row.join('.') || list_of_current_row.length <= 1) {
        //         // console.log("end of a subproof")
        //         // console.log(forms[current_form].children[5].children[0])
        //         forms[current_form].children[5].children[0].style.visibility = 'hidden'
        //     }
        // }
        // if (forms[current_form].children[0].children[0].value.split('.') <= 1) {
        //     console.log(`${current_form}-here`)
        //     // console.log(forms[current_form].children[5].children[0])
        //     forms[current_form].children[5].children[0].style.visibility = 'hidden'
        // }


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