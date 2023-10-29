let cookie = document.cookie
let csrf_token = cookie.substring(cookie.indexOf('=') + 1)

function getEl(selector) {
    return document.querySelector(selector);
}

function go_to_url(url) {
    window.location.href = url;
}

function create_card(url) {
    let form = getEl("#create-card-form");
    let form_data = new FormData(form);

    let selected = getEl("#deck-select").value;

    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token
        },
        success: function(resp) {
            form.reset();
            getEl("#deck-select").value = selected;
            console.log(resp);
        },
        contentType: false,
        processData: false
    });
}


