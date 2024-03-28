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
            e.preventDefault();
            let url = getEl("#view-deck-url").dataset.url;
            go_to_url(url + "/" + this.value);
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
