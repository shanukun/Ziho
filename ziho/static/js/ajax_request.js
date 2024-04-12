class AjaxRequest {
    constructor(
        url,
        form_data,
        success_fn,
        error_fn,
        form_id,
        show_toast = false,
        update_modal_form = false,
    ) {
        this.url = url;
        this.form_data = form_data;
        this.form_id = form_id;
        this.show_toast = show_toast;
        this.update_modal_form = update_modal_form;

        this.success_fn = (resp) => {};
        if (success_fn != null) {
            this.success_fn = success_fn;
        }
        this.error_fn = (resp) => {};
        if (error_fn) {
            this.error_fn = error_fn;
        }
    }

    _pre_response_op(resp, success = false) {
        if (success && this.update_modal_form) {
            getEl(`${this.form_id}`).innerHTML = resp.result.success_template;
        }
    }

    _post_request_op(resp, success = false) {
        // Update form only when there's a validation error.
        if (this.update_modal_form && resp.status == 406) {
            getEl(`${this.form_id}`).innerHTML =
                resp.responseJSON.message.result.error_template;
        } else if (this.show_toast) {
            let message = resp.message;
            if (!success) message = resp.responseJSON.message.message;
            display_toast(message, success);
        }

        bind_listeners();
    }

    make_request() {
        $.ajax({
            type: "POST",
            url: this.url,
            data: this.form_data,
            headers: {
                "X-CSRFTOKEN": csrf_token,
            },
            success: (resp) => {
                this._pre_response_op(resp, true);
                this.success_fn(resp);
                this._post_request_op(resp, true);
                do_reload();
            },
            error: (resp) => {
                this._pre_response_op(resp);
                this.error_fn(resp);
                this._post_request_op(resp);
            },
            contentType: false,
            processData: false,
        });
    }
}
