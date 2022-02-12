
window.onload = function () {

    const rightMenuSelection = localStorage.getItem("right-menu-selection");

    if (rightMenuSelection == "rules") {
        document.getElementById("rules").style.backgroundColor = "grey";
        document.getElementById("help").style.backgroundColor = "white";

        document.getElementById("rules-information").style.display = "block";
        document.getElementById("help-information").style.display = "none";

    }

    else if (rightMenuSelection == "help") {
        document.getElementById("rules").style.backgroundColor = "white";
        document.getElementById("help").style.backgroundColor = "grey";

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

        document.getElementById("rules").style.backgroundColor = "grey";
        document.getElementById("help").style.backgroundColor = "white";

        localStorage.setItem("right-menu-selection", "rules");
    }
    else if (e == 'help') {
        document.getElementById("rules-information").style.display = "none";
        document.getElementById("help-information").style.display = "block";

        document.getElementById("rules").style.backgroundColor = "white";
        document.getElementById("help").style.backgroundColor = "grey";

        localStorage.setItem("right-menu-selection", "help");

    }

}
