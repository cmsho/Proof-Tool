function insertTab(o, e) {
    replaceCharacter(o);

    var kC = e.keyCode ? e.keyCode : e.charCode ? e.charCode : e.which;
    if (kC == 9 && !e.shiftKey && !e.ctrlKey && !e.altKey) {
        var oS = o.scrollTop;
        if (o.setSelectionRange) {
            var sS = o.selectionStart;
            var sE = o.selectionEnd;
            o.value = o.value.substring(0, sS) + "\t" + o.value.substr(sE);
            o.setSelectionRange(sS + 1, sS + 1);
            o.focus();
        }
        else if (o.createTextRange) {
            document.selection.createRange().text = "\t";
            e.returnValue = false;
        }
        o.scrollTop = oS;
        if (e.preventDefault) {
            e.preventDefault();
        }
        return false;
    }
    return true;
}

function printOut() {
    let textInformation = document.getElementById('textbox').value;
    console.log(textInformation);
    alert(textInformation)
    return false;
}


// document.addEventListener('DOMContentLoaded', function(){
//     let txt = document.getElementById('premise');
//     txt.addEventListener('keydown',replaceCharacter);
// });

function replaceCharacter(ev) {
    console.log(document.getElementById(ev.id));
    let txt = document.getElementById(ev.id).value;
    console.log(txt);

    txt = txt.replace("\\and", "∧");
    txt = txt.replace("\\or", "∨");
    txt = txt.replace("\\implies", "→");
    txt = txt.replace("\\not", "¬");
    document.getElementById(ev.id).value = txt;




    // console.log(document.getElementById(ev.id));
    // console.log()
    // console.log(ev);
}

// function replaceCharacter(ev){
//     let txt = document.getElementById('premise').value;
//     console.log(txt);

//     txt = txt.replace("\\and","∧");
//     txt = txt.replace("\\or","∨");
//     txt = txt.replace("\\implies","→");
//     txt = txt.replace("\\not","¬");
//     document.getElementById('premise').value = txt;




//     console.log(document.getElementById('premise'));
//     // console.log()
//     // console.log(ev);
// }