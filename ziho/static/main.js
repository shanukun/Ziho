let cookie = document.cookie;
let csrf_token = cookie.substring(cookie.indexOf("=") + 1);

function getEl(selector) {
    return document.querySelector(selector);
}

function go_to_url(url) {
    window.location.href = url;
}

function create_card(url) {
    let form = getEl("#create-card-form");
    let form_data = new FormData(form);

    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token,
        },
        success: function (resp) {
            form.reset();
            getEl("#deck-select").value;
            console.log(resp);
        },
        contentType: false,
        processData: false,
    });
}

function save_card(card) {
    let url = getEl("#save-card-url").dataset.url;
    console.log(url);
    let form_data = new FormData();

    form_data.append("deck_id", card.deck_id);
    form_data.append("card_id", card.card_id);
    form_data.append("csrf_token", csrf_token);
    Object.keys(card.card_info).forEach((key) => {
        form_data.append(key, card.card_info[key]);
    });
    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token,
        },
        success: function (resp) {
            console.log(resp);
        },
        contentType: false,
        processData: false,
    });
}

function get_cards(url, deck_id) {
    let form_data = new FormData();
    form_data.append("deck_id", deck_id);

    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token,
        },
        success: function (resp) {
            console.log(resp);
            if (!resp.status) {
                console.log("Failed");
                return;
            }

            const displayer = new Displayer();
            displayer.fill_queue(resp.result);
            displayer.show_card();
        },
        contentType: false,
        processData: false,
    });
}
