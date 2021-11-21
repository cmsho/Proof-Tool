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

function add_new_form(event){
    if (event){
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

function delete_form(button){
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
            if (x==0) {
                input.setAttribute('name', `form-${i}-line_no`)
                input.setAttribute('id', `id_form-${i}-line_no`) 
            }
            if (x==1) {
                input.setAttribute('name', `form-${i}-formula`)
                input.setAttribute('id', `id_form-${i}-formula`)
            }
            if (x==2) {
                input.setAttribute('name', `form-${i}-rule`)
                input.setAttribute('id', `id_form-${i}-rule`)
            }
            if (x==3) {
                input.setAttribute('id', `delete-btn-${i}`)
            }  
        }
    }
}