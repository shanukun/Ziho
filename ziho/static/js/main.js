let cookie = document.cookie;
let csrf_token = cookie.substring(cookie.indexOf("=") + 1);

let RELOAD_PAGE = false;
const do_reload = () => {
    RELOAD_PAGE = true;
};
const may_reload = () => {
    let reload = false;
    if (RELOAD_PAGE) {
        reload = true;
        RELOAD_PAGE = false;
    }
    return reload;
};

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

function display_toast(msg, success = true) {
    const temp_html = getEl("#toast-template").content.cloneNode(true);
    const toast_id = "toast_" + toast_counter++;

    getEl(".toast-container").appendChild(temp_html);

    const el = getEl("#toast_0");
    el.setAttribute("id", toast_id);
    getEl(`#${toast_id} .toast-body`).innerHTML = msg;

    let rect_class = success ? "rect-success" : "rect-danger";
    getEl(`#${toast_id} rect`).setAttribute("class", rect_class);

    const toastEl = document.getElementById(toast_id);
    const toast = new bootstrap.Toast(toastEl, (options = { autohide: true }));
    toast.show();
}

function show_uploaded_image(el, image) {
    let invalid_feedback = getEl(
        ".card-back-image > .is-invalid ~ .invalid-feedback",
    );
    if (typeof invalid_feedback != "undefined" && invalid_feedback != null) {
        invalid_feedback.classList.add("d-none");
    }

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

const all_form_listener = [
    {
        el_sel: "#upload-post-image",
        event: "change",
        func: (e) => {
            change_preview_image(e.target);
        },
    },
    {
        el_sel: "#view-deck-card-select",
        event: "change",
        func: (e) => {
            let url = getEl("#view-deck-url").dataset.url;
            go_to_url(url + "/" + e.target.value);
        },
    },
];

const bind_events = (el, event, func) => {
    el.addEventListener(event, func);
};

const bind_listeners = () => {
    all_form_listener.forEach((o) => {
        el = getEl(o.el_sel);
        if (el != undefined && el != null) {
            bind_events(el, o.event, o.func);
        }
    });
};
