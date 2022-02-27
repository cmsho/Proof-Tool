
window.onload = function () {

    const rightMenuSelection = localStorage.getItem("right-menu-selection");

    if (rightMenuSelection == "rules") {

        document.getElementById("rules").classList.remove('btn-secondary');
        document.getElementById("rules").classList.add('btn-primary');
        document.getElementById("help").classList.remove('btn-primary');
        document.getElementById("help").classList.add('btn-secondary');

        document.getElementById("rules-information").style.display = "block";
        document.getElementById("help-information").style.display = "none";

    }

    else if (rightMenuSelection == "help") {

        document.getElementById("rules").classList.remove('btn-primary');
        document.getElementById("rules").classList.add('btn-secondary');
        document.getElementById("help").classList.remove('btn-secondary');
        document.getElementById("help").classList.add('btn-primary');

        document.getElementById("rules-information").style.display = "none";
        document.getElementById("help-information").style.display = "block";

    }
};



function showInformation(e) {
    console.log(e);

    var button = document.getElementById(e);

    if (e == "rules") {
        document.getElementById("rules-information").style.display = "block";
        document.getElementById("help-information").style.display = "none";


        document.getElementById("rules").classList.remove('btn-secondary');
        document.getElementById("rules").classList.add('btn-primary');
        document.getElementById("help").classList.remove('btn-primary');
        document.getElementById("help").classList.add('btn-secondary');

        localStorage.setItem("right-menu-selection", "rules");
    }
    else if (e == 'help') {
        document.getElementById("rules-information").style.display = "none";
        document.getElementById("help-information").style.display = "block";


        document.getElementById("rules").classList.remove('btn-primary');
        document.getElementById("rules").classList.add('btn-secondary');
        document.getElementById("help").classList.remove('btn-secondary');
        document.getElementById("help").classList.add('btn-primary');

        localStorage.setItem("right-menu-selection", "help");

    }

}

function showRules(e) {
    console.log(e)

    if (e === "TFL-Button") {
        console.log("TFL")
        document.getElementById("TFL-Rules").style.display = "block";
        document.getElementById("FOL-Rules").style.display = "none";


        document.getElementById("TFL-Button").classList.remove('btn-outline-secondary');
        document.getElementById("TFL-Button").classList.add('btn-outline-primary');
        document.getElementById("FOL-Button").classList.remove('btn-outline-primary');
        document.getElementById("FOL-Button").classList.add('btn-outline-secondary');

        localStorage.setItem("right-menu-selection", "TFL-Rules");

    }
    else if (e === "FOL-Button") {
        console.log("FOL")
        document.getElementById("TFL-Rules").style.display = "none";
        document.getElementById("FOL-Rules").style.display = "block";


        document.getElementById("TFL-Button").classList.remove('btn-outline-primary');
        document.getElementById("TFL-Button").classList.add('btn-outline-secondary');
        document.getElementById("FOL-Button").classList.remove('btn-outline-secondary');
        document.getElementById("FOL-Button").classList.add('btn-outline-primary');


        localStorage.setItem("right-menu-selection", "FOL-Rules");
    }

}