function add_problem() {
        document.getElementById('hx-btn').click();
        setTimeout(() => {}, 200);
}

function mutate(mutations) {
        window.location = "/problems/add?assignment=" + target.innerText
}

var target = document.querySelector('div#returnValue')
var observer = new MutationObserver( mutate );
var config = { characterData: false, attributes: false, childList: true, subtree: false };

observer.observe(target, config);
