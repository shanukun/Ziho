function get_form_data(form_id = null) {
    let form_data;
    if (form_id) {
        form_data = new FormData(getEl(form_id));
    } else {
        form_data = new FormData();
        form_data.append("csrf_token", csrf_token);
    }
    return form_data;
}

const create_deck = (url, form_id) => {
    let form_data = get_form_data(form_id);
    const success_fn = () => {
        console.log("Calling create_deck success fn.");
    };
    new AjaxRequest(
        url,
        form_data,
        success_fn,
        null,
        form_id,
        true,
        (update_modal_form = true),
    ).make_request();
};

function add_card(url, form_id) {
    let form_data = get_form_data(form_id);

    const success_fn = (resp) => {
        // store selected deck to reset on form update
        let selected = getEl("#add-card-deck-select").value;
        getEl("#add-card-form").reset();
        getEl("#add-card-deck-select").value = selected;
        getEl("#uploaded-image-preview").setAttribute("class", "d-none");
    };
    new AjaxRequest(
        url,
        form_data,
        success_fn,
        null,
        form_id,
        true,
        (update_modal_form = true),
    ).make_request();
}

function update_card(url, form_id) {
    let form_data = get_form_data(form_id);

    // Only send image if it is updated.
    if (
        typeof $("#upload-post-image").data("prev_image_path") !== "undefined"
    ) {
        if (
            form_data.get("image") ===
            $("#upload-post-image").data("prev_image_path")
        ) {
            form_data.set("image", null);
        }
    }

    new AjaxRequest(
        url,
        form_data,
        null,
        null,
        form_id,
        true,
        true,
    ).make_request();
}

function save_card(card) {
    let url = getEl("#save-card-url").dataset.url;
    let form_data = get_form_data();

    form_data.append("deck_id", card.deck.deck_id);
    form_data.append("card_id", card.card.card_id);
    Object.keys(card.card_info).forEach((key) => {
        form_data.append(key, card.card_info[key]);
    });

    const success_fn = (resp) => {
        console.log(resp);
    };
    new AjaxRequest(
        url,
        form_data,
        success_fn,
        null,
        null,
        false,
        false,
    ).make_request();
}

function get_cards(url, deck_id, deck_name) {
    $("#study-card-title").html = deck_name;
    let form_data = get_form_data();
    form_data.append("deck_id", deck_id);

    const success_fn = (resp) => {
        const displayer = new Displayer(deck_name);
        displayer.fill_queue(resp.result);
        displayer.show_card();
    };
    new AjaxRequest(
        url,
        form_data,
        success_fn,
        null,
        null,
        false,
        false,
    ).make_request();
}

const form_route = {
    "#create-deck-form": create_deck,
    "#add-card-form": add_card,
    "#update-card-form": update_card,
};

const submit_form = (e) => {
    e.preventDefault();
    e.stopPropagation();
    let url = e.target.action;
    let form_id = "#" + e.target.id;
    form_route[form_id](url, form_id);
};
