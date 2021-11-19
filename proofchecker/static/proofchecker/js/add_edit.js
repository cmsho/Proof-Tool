const addMoreBtn = document.getElementById("add-more")
const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
const currentProofLineForms = document.getElementsByClassName("proofline-form")
addMoreBtn.addEventListener("click", add_new_form)


function add_new_form(button) {

    let currentFormCount = currentProofLineForms.length
    const formCopyTarget = document.getElementById("proof-line-list")

    const emptyFormElement = document.getElementById("empty-form").cloneNode(true)
    emptyFormElement.setAttribute("class", "proofline-form")
    emptyFormElement.setAttribute("id", `proofline-form-${currentFormCount}`)

    const regex = new RegExp('__prefix__', 'g')
    emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1)
    formCopyTarget.append(emptyFormElement)
}


function removeProofline(button) {
    var id = button.id.replace(/[^0-9]/g, "")
    console.log("ID: " + id)
    const mark_deleted = document.getElementById("id_form-" + id + "-DELETE")
    console.log("MARK_DELETED: " + mark_deleted.id)
    mark_deleted.setAttribute("checked", "true")
    const targeted_proofline = document.getElementById("proofline-form-" + id)
    console.log("TARGETED_PROOFLINE: " + targeted_proofline.id)
    targeted_proofline.hidden = true
}

const inputFields = document.getElementsByClassName("text-replacement-enabled")
for (let i of inputFields){
    // console.log(i)
    i.setAttribute("onkeydown", "replaceCharacter(this);")
}