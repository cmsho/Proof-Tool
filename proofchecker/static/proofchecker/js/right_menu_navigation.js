function showInformation(e) {
    console.log(e);

    var button = document.getElementById(e);

    if (e == 'info') {
        document.getElementById("info-information").style.display = "block";
        document.getElementById("rules-information").style.display = "none";
        document.getElementById("other-information").style.display = "none";

    } else if (e == "rules") {
        document.getElementById("info-information").style.display = "none";
        document.getElementById("rules-information").style.display = "block";
        document.getElementById("other-information").style.display = "none";
    } else if (e == "other") {
        document.getElementById("info-information").style.display = "none";
        document.getElementById("rules-information").style.display = "none";
        document.getElementById("other-information").style.display = "block";
    }
}
