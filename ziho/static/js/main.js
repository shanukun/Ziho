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

let toast_counter = 1;

function show_toast(msg, success = true) {
    const temp_html = getEl("#toast-template").content.cloneNode(true);
    const toast_id = "toast_" + toast_counter++;

    getEl(".toast-container").appendChild(temp_html);

    const el = getEl("#toast_0");
    el.setAttribute("id", toast_id);
    getEl(`#${toast_id} .toast-body`).innerHTML = msg;

    let rect_class = "rect-success";
    if (!success) {
        rect_class = "rect-danger";
    }
    getEl(`#${toast_id} rect`).setAttribute("class", rect_class);

    const toastEl = document.getElementById(toast_id);
    const toast = new bootstrap.Toast(toastEl, (options = { autohide: true }));
    toast.show();
}

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

function make_ajax_request(
    url,
    form_data,
    success_fn,
    error_fn,
    toast = false,
) {
    if (!success_fn) success_fn = () => {};
    if (!error_fn) error_fn = () => {};

    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token,
        },
        success: (resp) => {
            success_fn(resp);
            if (toast) show_toast(resp.message);
        },
        error: (resp) => {
            error_fn(resp);
            if (toast) show_toast(resp.responseText);
        },
        contentType: false,
        processData: false,
    });
}

function update_card(url) {
    let form_data = get_form_data("#update-card-form");

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

    make_ajax_request(url, form_data, null, null, true);
}

function add_card(url) {
    let form_data = get_form_data("#add-card-form");
    let selected = getEl("#add-card-deck-select").value;

    const success_fn = (resp) => {
        console.log(resp);
        let form = getEl("#add-card-form");
        form.reset();
        getEl("#add-card-deck-select").value = selected;
        getEl("#uploaded-image-preview").setAttribute("class", "d-none");
    };
    make_ajax_request(url, form_data, success_fn, null, true);
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
    make_ajax_request(url, form_data, success_fn, null, true);
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
    make_ajax_request(url, form_data, success_fn, null);
}

function show_uploaded_image(el, image) {
    el.setAttribute("src", image);
    el.classList.add("d-flex");
    el.classList.remove("d-none");
}

function change_preview_image(input) {
    let preview = getEl("#uploaded-image-preview");

    let reader;
    if (input.files && input.files[0]) {
        reader = new FileReader();

        reader.onload = function (e) {
            show_uploaded_image(preview, e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
