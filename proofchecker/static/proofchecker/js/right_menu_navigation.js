
window.onload = function () {

    const rightMenuSelection = localStorage.getItem("right-menu-selection");

    if (rightMenuSelection == "rules") {
        document.getElementById("info").style.backgroundColor = "white";
        document.getElementById("rules").style.backgroundColor = "grey";
        document.getElementById("other").style.backgroundColor = "white";

        document.getElementById("info-information").style.display = "none";
        document.getElementById("rules-information").style.display = "block";
        document.getElementById("other-information").style.display = "none";

    } else if (rightMenuSelection == "other") {
        document.getElementById("info").style.backgroundColor = "white";
        document.getElementById("rules").style.backgroundColor = "white";
        document.getElementById("other").style.backgroundColor = "grey";

        document.getElementById("info-information").style.display = "none";
        document.getElementById("rules-information").style.display = "none";
        document.getElementById("other-information").style.display = "block";



    } else if (rightMenuSelection == "info") {
        document.getElementById("info").style.backgroundColor = "grey";
        document.getElementById("rules").style.backgroundColor = "white";
        document.getElementById("other").style.backgroundColor = "white";

        document.getElementById("info-information").style.display = "block";
        document.getElementById("rules-information").style.display = "none";
        document.getElementById("other-information").style.display = "none";

    }
};



function showInformation(e) {
    console.log(e);

    var button = document.getElementById(e);

    if (e == 'info') {
        document.getElementById("info-information").style.display = "block";
        document.getElementById("rules-information").style.display = "none";
        document.getElementById("other-information").style.display = "none";

        document.getElementById("info").style.backgroundColor = "grey";
        document.getElementById("rules").style.backgroundColor = "white";
        document.getElementById("other").style.backgroundColor = "white";

        localStorage.setItem("right-menu-selection", "info");

    } else if (e == "rules") {
        document.getElementById("info-information").style.display = "none";
        document.getElementById("rules-information").style.display = "block";
        document.getElementById("other-information").style.display = "none";

        document.getElementById("info").style.backgroundColor = "white";
        document.getElementById("rules").style.backgroundColor = "grey";
        document.getElementById("other").style.backgroundColor = "white";

        localStorage.setItem("right-menu-selection", "rules");
    } else if (e == "other") {
        document.getElementById("info-information").style.display = "none";
        document.getElementById("rules-information").style.display = "none";
        document.getElementById("other-information").style.display = "block";

        document.getElementById("info").style.backgroundColor = "white";
        document.getElementById("rules").style.backgroundColor = "white";
        document.getElementById("other").style.backgroundColor = "grey";


        localStorage.setItem("right-menu-selection", "other");
    }
}
