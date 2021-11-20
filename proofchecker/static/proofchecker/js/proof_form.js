// Add new line
document.addEventListener('click', (event)=> {
    if (event.target.id == 'add-more') {
        add_new_form(event);
    }
})
function add_new_form(event){
    if (event){
        event.preventDefault()
    }
    const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
    const currentProofLineForms = document.getElementsByClassName("proofline-form")
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


// Symbol replacement functionality for input fields
function replaceCharacter(ev) {
    console.log(document.getElementById(ev.id));
    let txt = document.getElementById(ev.id).value;
    console.log(txt);

    txt = txt.replace("\\and", "∧");
    txt = txt.replace("\\or", "∨");
    txt = txt.replace("\\implies", "→");
    txt = txt.replace("\\not", "¬");
    txt = txt.replace("\\iff", "↔");
    txt = txt.replace("\\contradiction", "⊥");
    document.getElementById(ev.id).value = txt;
}