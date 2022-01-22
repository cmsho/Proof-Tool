
// ---------------------------------------------------------------------------------------------------------------------
// list of variables  to store dom element ids/classes/names (difference between inlineformset vs modelformset
// ---------------------------------------------------------------------------------------------------------------------
const FORMSET_PREFIX                = "proofline_set";                 // for modelformset - "form-"
const FORMSET_TOTALFORMS_ID         = "id_proofline_set-TOTAL_FORMS";   // for modelformset - "id_form-TOTAL_FORMS"
const FORMSET_TBODY_ID              = "proofline-list";                 // for modelformset - "proofline-list"
const FORMSET_TR_CLASS              = "proofline_set";                 // for modelformset - "proofline-form"

// ---------------------------------------------------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', reloadPage(), false);

function reloadPage(){
    //this function will run on page load

    //will sort proof table based on ORDER field
    sortTable()
    //will decide which button to display between start and restart
    setStartRestartButtonAtBeginning()
}
// ---------------------------------------------------------------------------------------------------------------------


// ---------------------------------------------------------------------------------------------------------------------
// Helper functions
// ---------------------------------------------------------------------------------------------------------------------

// Helper function to set multiple attributes at once
function setAttributes(el, attrs) {
    for (var key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}

// Call this at end of any function that changes the amount of forms
function update_form_count() {
    const formsetManagerTotalFormCounter = document.getElementById(FORMSET_TOTALFORMS_ID)
    let currentFormCount = document.getElementsByClassName(FORMSET_TR_CLASS).length
    formsetManagerTotalFormCounter.setAttribute('value', currentFormCount)
}

// Call this at the end of any function that changes the amount of forms

function update_form_ids() {
    const forms = document.getElementsByClassName(FORMSET_TR_CLASS)
    const fields = ['line_no', 'formula', 'rule', 'insert-btn', 'create-subproof-btn', 'conclude-subproof-btn', 'delete-btn', 'id', 'DELETE', 'ORDER']

    for (i = 0; i < forms.length; i++) {

        // Update the ID of each table row
        forms[i].setAttribute('id', `${FORMSET_PREFIX}-${i}`)

        // Update the ID of each input field (nested in <td>)
        var tds = forms[i].children
        for (x = 0; x < fields.length-1; x++) {
            // Input field is child of <td>
            var input = tds[x].children[0]
            input.setAttribute('name', `${FORMSET_PREFIX}-${i}-${fields[x]}`)
            input.setAttribute('id', `id_${FORMSET_PREFIX}-${i}-${fields[x]}`)
        }

        // Set last three fields
    }
}

function get_total_forms_count() {
    return document.getElementsByClassName(FORMSET_TR_CLASS).length
}

function get_total_forms_count_in_manager() {
    return parseInt(document.getElementById(FORMSET_TOTALFORMS_ID).value)
}

function get_total_formset_count_in_manager(){
    return parseInt(document.getElementById('id_proofline_set-TOTAL_FORMS').value)
}

function set_total_forms_count_in_manager(value) {
    document.getElementById(FORMSET_TOTALFORMS_ID).setAttribute('value', value)
   
}

function set_total_formset_count_in_manager(value){
    document.getElementById('id_'+FORMSET_PREFIX+'-TOTAL_FORMS').setAttribute('value', value);
}

function create_empty_form(index) {
    const emptyFormElement = document.getElementById('empty-form').cloneNode(true)
    emptyFormElement.setAttribute("class", FORMSET_TR_CLASS)
    emptyFormElement.setAttribute("id", `${FORMSET_PREFIX}-${index}`)
    const regex = new RegExp('__prefix__', 'g')
    emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, index)
    return emptyFormElement
}

function get_form_id(obj) {
    return parseInt(obj.id.replace(/[^0-9]/g, ""))
}

// Delete children from any DOM element
function delete_children(element) {
        var first = element.firstElementChild;
        while (first) {
            first.remove();
            first = element.firstElementChild;
        }
}

function reset_positional_index(){
    const ORDER_fields = document.querySelectorAll('[id $= "-ORDER"]');
    var pos_index = 0;
    var index = null
    for (let field of ORDER_fields){
        if (field.id != null && field.id.indexOf("__prefix__")<0){
            index = get_form_id(field)
            if (!document.getElementById(`${FORMSET_PREFIX}-${index}`).hidden){
                field.value = pos_index++
                document.getElementById(`id_${FORMSET_PREFIX}-${index}-ORDER`).value = field.value
            } else {
                field.value = -1
            }

        }
    }
}

function sortTable() {
    var i, x, y;
    var switching = true;

    // Run loop until no switching is needed
    while (switching) {
        switching = false;
        var rows = document.getElementsByClassName(FORMSET_TR_CLASS)
        // Loop to go through all rows
        for (i = 1; i < (rows.length - 1); i++) {
            var switch_flag = false;

            // Fetch 2 elements that need to be compared
            x = rows[i].getElementsByTagName("input")[9].value
            y = rows[i+1].getElementsByTagName("input")[9].value
            console.log(x)

            // Check if 2 rows need to be switched
            if (parseInt(x) > parseInt(y)) {
                // If yes, mark Switch as needed and break loop
                switch_flag = true;
                break;
            }
        }
        if (switch_flag) {
            // Function to switch rows and mark switch as completed
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}


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

function get_row(index) {

    var row_object = document.getElementById(FORMSET_PREFIX + '-' + (index))
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

// ---------------------------------------------------------------------------------------------------------------------


function setStartRestartButtonAtBeginning(){
    if (document.getElementById(`id_${FORMSET_PREFIX}-0-rule`)!=null && document.getElementById(`id_${FORMSET_PREFIX}-0-rule`).value != ''){
        document.getElementById("btn_start_proof").hidden = true
        document.getElementById("btn_restart_proof").classList.remove("hidden")
    }
}

// Automatically populate the premise values
function start_proof(element) {
    var premises = document.getElementById('id_premises').value
    var premiseArray = premises.split(",").map(item => item.trim())
    var prooflineTableBody = document.getElementById(FORMSET_TBODY_ID)
    
    for (i = 0; i < premiseArray.length; i++) {
        var newRow = create_empty_form(i)
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
        prooflineTableBody.appendChild(newRow)
    }
    update_form_count()
    hide_conclude_button()
    element.hidden=true
    document.getElementById("btn_restart_proof").classList.remove("hidden")
    reset_positional_index()
}

//restart proof
function restart_proof(element){
    var prooflineList = document.getElementById(FORMSET_TBODY_ID)
    delete_children(prooflineList)
    start_proof(document.getElementById("btn_start_proof"))
}



// ---------------------------------------------------------------------------------------------------------------------
// INSERT FUNCTIONS
// ---------------------------------------------------------------------------------------------------------------------

// Inserts form below current line
function insert_form(obj) {
    insert_form_helper(get_form_id(obj) + 1)
    insert_row_current_level(get_form_id(obj))
    hide_conclude_button()
    reset_positional_index()
}

function insert_form_helper(index) {
    const getNextIndex = get_total_forms_count();
    const emptyFormElement = create_empty_form(getNextIndex)
    const proof_tbody = document.getElementById(FORMSET_TBODY_ID)
    const proof_table_row = document.getElementById(FORMSET_PREFIX + '-' + (index - 1))
    if (proof_table_row != null) {
        proof_table_row.after(emptyFormElement)
    } else {
        proof_tbody.append(emptyFormElement)
    }
    update_form_ids()
    update_form_count()
    reset_positional_index()
}

function insert_row_current_level(index) {
    // Get the button row
    var button_row = get_row(index)

    // If it has no subproof numbering then add one to the previous row number
    if (button_row.prefix_of_row.length == 0) {
        document.getElementById(FORMSET_PREFIX + '-' + (index + 1)).children[0].children[0].value = `${Number(button_row.line_number_of_row) + 1}`
    }
    // if it has subproof number then take the last number and add one to it
    else {
        document.getElementById(FORMSET_PREFIX + '-' + (index + 1)).children[0].children[0].value = `${button_row.string_of_prefix}.${Number(button_row.final_value) + 1}`
    }
    var direction = 1;
    var starting_point = index + 2

    var prefix_value_list = button_row.prefix_of_row.length >= 1 ? button_row.prefix_of_row : []
    renumber_rows(direction, starting_point, prefix_value_list)
    reset_positional_index()
}

function renumber_rows(direction, starting_point, prefix_value_list) {

    // Forms that you'll iterate over
    const forms = document.getElementsByClassName(FORMSET_TR_CLASS)
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
}


// ---------------------------------------------------------------------------------------------------------------------
// SUBBPROOF FUNCTIONS
// ---------------------------------------------------------------------------------------------------------------------

function create_subproof(obj) {
    insert_form_helper(get_form_id(obj) + 1)

    generate_new_subproof_row_number(get_form_id(obj) + 1)
    hide_conclude_button()
    reset_positional_index()
}

function conclude_subproof(obj) {
    insert_form_helper(get_form_id(obj) + 1)

    insert_row_parent_level(get_form_id(obj))
    hide_conclude_button()
    reset_positional_index()
}


function generate_new_subproof_row_number(index) {

    // Get the row that the button was clicked
    var row_number_of_clicked_button = document.getElementById(FORMSET_PREFIX + '-' + (index - 1)).children[0].children[0].value
    const original_row_number_of_clicked_button = row_number_of_clicked_button

    // Update row number of clicked button
    document.getElementById(FORMSET_PREFIX + '-' + (index - 1)).children[0].children[0].value = `${original_row_number_of_clicked_button}.1`
    document.getElementById(FORMSET_PREFIX + '-' + (index - 1)).children[2].children[0].value = 'Assumption'



    // Update the row number of the new row
    document.getElementById(FORMSET_PREFIX + '-' + (index)).children[0].children[0].value = `${original_row_number_of_clicked_button}.2`

}


function insert_row_parent_level(index) {
    var button_row = get_row(index)

    // Get prefix of the new row number
    var new_row_number = button_row.prefix_of_row
    // Add one to the final value of the new_row_number
    new_row_number[new_row_number.length - 1] = `${Number(new_row_number[new_row_number.length - 1]) + 1}`
    // Construct new row number string and attach it to the new row
    document.getElementById(FORMSET_PREFIX + '-' + (index + 1)).children[0].children[0].value = new_row_number.join('.')

    var direction = 1
    var starting_point = index + 2
    // if it's an integer than use an empty list for the prefix
    var prefix_value_list = new_row_number.length > 1 ? new_row_number : []


    // console.log(button_row.prefix_of_row)

    var prefix_value_list = button_row.prefix_of_row.length > 1 ? button_row.prefix_of_row : []

    renumber_rows(direction, starting_point, prefix_value_list)
    reset_positional_index()
}


// Adds new form at end of table
function add_form(event) {
    if (event) {
        event.preventDefault()
    }
    const totalNewForms = document.getElementById(FORMSET_TOTALFORMS_ID)
    const currentProofLineForms = document.getElementsByClassName(FORMSET_TR_CLASS)
    let currentFormCount = currentProofLineForms.length
    const formCopyTarget = document.getElementById(FORMSET_TBODY_ID)
    emptyFormElement = create_empty_form()
    emptyFormElement.setAttribute("id", `${FORMSET_PREFIX}-${currentFormCount}`)
    const regex = new RegExp('__prefix__', 'g')
    emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, currentFormCount)

    // Added by Thomas Below
    if (currentFormCount > 0) {
        var previous_row_number = document.getElementById(FORMSET_PREFIX + '-' + (currentFormCount - 1)).children[0].children[0].value
        var new_row_number = `${Number(previous_row_number[0]) + 1}`
    } else {
        var new_row_number = '1'
    }
    emptyFormElement.children[0].children[0].setAttribute("value", new_row_number)
    // emptyFormElement.children[0].children[0].setAttribute("readonly", true)
    // Added by Thomas Above
    formCopyTarget.append(emptyFormElement)
    update_form_count()
    hide_conclude_button()
    reset_positional_index()
}


// ---------------------------------------------------------------------------------------------------------------------
// DELETE FUNCTIONS
// ---------------------------------------------------------------------------------------------------------------------

function delete_form(obj){
    remove_from_proofline_formset(get_form_id(obj))
}

function remove_from_proofline_formset(index) {
    //mark checkbox true

    document.getElementById('id_'+FORMSET_PREFIX+'-' + index + '-DELETE').setAttribute("checked", "true")
    // document.getElementById('id_'+FORMSET_PREFIX+'-' + index + '-line_no').setAttribute("value", "*del*")
    //hide row
    // document.getElementById(FORMSET_PREFIX+'-' + index).hidden = true;

    //if id fields is empty that means this deleted (hidden now) row is a new row.. not existing one.. so we can actually remove it.
    if (document.getElementById('id_'+FORMSET_PREFIX+'-' + index + '-id').value == ''){
        document.getElementById(FORMSET_PREFIX+'-' + index).remove()
        pull_up_proofline_forms(index)
        set_total_formset_count_in_manager(get_total_formset_count_in_manager()-1)
    }
    reset_positional_index()
}

function pull_up_proofline_forms(to_index){
    const last_form_element_id = get_total_formset_count_in_manager() - 1;
    for (let i = to_index+1; i <= last_form_element_id; i++) {
      change_proofline_form_id(i, i-1)
    }
}

function change_proofline_form_id(old_id, new_id){
    const targeted_element = document.getElementById('proofline_set-'+old_id)
    if (targeted_element != null) {
        document.getElementById('proofline_set-' + old_id).setAttribute('id', `proofline_set-${new_id}`)
        const fields = ['id', 'ORDER', 'DELETE', 'line_no', 'formula', 'rule'];
        fields.forEach(function (field) {
            document.getElementById('id_proofline_set-' + old_id + '-' + field).setAttribute('name', `proofline_set-${new_id}-${field}`)
            document.getElementById('id_proofline_set-' + old_id + '-' + field).setAttribute('id', `id_proofline_set-${new_id}-${field}`)
        })
        document.getElementById('id-form-btn-insert-row-' + old_id).setAttribute('id', `id-form-btn-insert-row-${new_id}`)
        document.getElementById('id-form-btn-delete-row-' + old_id).setAttribute('id', `id-form-btn-delete-row-${new_id}`)
    }
}

function delete_form_old(obj) {
    var index = get_form_id(obj)
    var forms = document.getElementsByClassName(FORMSET_TBODY_ID)
    var index_of_last_row = forms.length - 1

    if (index != 0) {
        var above_row = get_row(index - 1)
    }
    var button_row = get_row(index)

    if (index != index_of_last_row) {
        var below_row = get_row(index + 1)
    }

    // Delete row
    const form_to_delete = document.getElementById(FORMSET_PREFIX + '-' + index)
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

    hide_conclude_button()

}


function hide_conclude_button() {

    const forms = document.getElementsByClassName(FORMSET_TBODY_ID)
    var number_of_forms = forms.length - 1

    for (var current_form = 0; current_form <= number_of_forms; current_form++) {
        var current_row = get_row(current_form)
        if (current_form == 0) {
            document.getElementById(`${FORMSET_PREFIX}-${current_form}`).children[6].children[0].style.visibility = 'hidden'
        }
        else if (current_form < number_of_forms) {
            var next_row = get_row(current_form + 1)
            if (current_row.string_of_prefix == next_row.string_of_prefix) {
                document.getElementById(`${FORMSET_PREFIX}-${current_form}`).children[6].children[0].style.visibility = 'hidden'
            }
        } else if (current_row.list_of_line_number.length <= 1) {
            document.getElementById(`${FORMSET_PREFIX}-${current_form}`).children[6].children[0].style.visibility = 'hidden'
            break
        }
    }
}
