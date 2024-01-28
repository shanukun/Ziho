let cookie = document.cookie;
let csrf_token = cookie.substring(cookie.indexOf("=") + 1);

function getEl(selector) {
    return document.querySelector(selector);
}

function go_to_url(url) {
    window.location.href = url;
}

// increase textarea height depending on the length of the text
$("textarea")
    .each(function () {
        this.setAttribute(
            "style",
            "height:" + this.scrollHeight + "px;overflow-y:hidden;",
        );
    })
    .on("focus input", function () {
        this.style.height = 0;
        this.style.height = this.scrollHeight + "px";
    });

function delete_card(url) {
    let form = getEl("#delete-card-form");
    let form_data = new FormData(form);

    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token,
        },
        // TODO handle fail case
        success: function (resp) {
            // location.reload();
            console.log(resp);
        },
        contentType: false,
        processData: false,
    });

}

function update_card(url) {
    let form = getEl("#update-card-form");
    let form_data = new FormData(form);

    // Only send image if it's updated.
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

    for (const pair of form_data.entries()) {
        console.log(`${pair[0]}, ${pair[1]}`);
    }

    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token,
        },
        // TODO handle fail case
        success: function (resp) {
            location.reload();
            console.log(resp);
        },
        contentType: false,
        processData: false,
    });
}

function add_card(url) {
    let form = getEl("#add-card-form");
    let form_data = new FormData(form);

    let selected = getEl("#add-card-deck-select").value;

    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token,
        },
        // TODO handle fail case
        success: function (resp) {
            form.reset();
            getEl("#add-card-deck-select").value = selected;
            getEl("#uploaded-image-preview").classList.toggle("d-none");
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

function get_cards(url, deck_id, deck_name) {
    $("#study-card-title").html = deck_name;
    let form_data = new FormData();
    form_data.append("deck_id", deck_id);
    form_data.append("csrf_token", csrf_token);

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

            const displayer = new Displayer(deck_name);
            displayer.fill_queue(resp.result);
            displayer.show_card();
        },
        contentType: false,
        processData: false,
    });
}

function show_uploaded_image(el, image) {
    el.setAttribute("src", image);
    el.classList.add("d-flex");
    el.classList.remove("d-none");
}

function change_preview_image(input) {
    let reader;
    let preview = getEl("#uploaded-image-preview");

    if (input.files && input.files[0]) {
        reader = new FileReader();

        reader.onload = function (e) {
            show_uploaded_image(preview, e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
