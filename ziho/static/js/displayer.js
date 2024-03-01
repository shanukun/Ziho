class Scheduler {
    constructor() {
        this.f = new FSRS();
    }

    check_graduation(card, rating) {
        const s_card = this.f.repeat(card, new Date())[rating].card;
        // console.log(s_card.due);

        let queue_rating = QueueRank.Good;
        if (s_card.due < new Date(Date.now() + 5 * 60 * 1000)) {
            queue_rating = QueueRank.Again;
        } else if (s_card.due < new Date(Date.now() + 10 * 60 * 1000)) {
            queue_rating = QueueRank.Hard;
        }

        console.log(JSON.stringify(s_card));

        return {
            graduated: s_card.scheduled_days > 0 ? true : false,
            queue: queue_rating,
            card_info: JSON.parse(JSON.stringify(s_card)),
        };
    }

    static toCard(card_info) {
        let card = Object.assign(Card.prototype, card_info);
        card.last_review = new Date(card.last_review);
        card.due = new Date(card.due);
        return card;
    }
}

function add_remove_html_class(elem, to_be_added, to_be_removed) {
    elem.classList.remove(to_be_removed);
    elem.classList.add(to_be_added);
}

class Displayer {
    constructor(deck_name) {
        this.cards = new CardQueue();
        this.scheduler = new Scheduler();

        this.deck_name = deck_name;
        this.currentCard = undefined;

        this._init_template();
    }

    _init_template() {
        getEl("#study-deck-title").innerHTML = this.deck_name;
        const temp_html = getEl("#study-deck-template").content.cloneNode(true);

        getEl("#study-deck-modal-content").innerHTML = "";
        getEl("#study-deck-modal-content").appendChild(temp_html);

        const cardRatingClickHandler = (e) => {
            const card_rating = e.target.dataset.rating;
            const card = this.scheduler.check_graduation(
                Scheduler.toCard(this.currentCard.card_info),
                card_rating,
            );

            this.currentCard.card_info = card.card_info;
            if (card.graduated) {
                save_card(this.currentCard);
            } else {
                this.cards.insert(this.currentCard, card.queue);
            }

            this.show_card();
            return;
        };

        (() => {
            const el_id_list = [
                "#again-card",
                "#hard-card",
                "#good-card",
                "#easy-card",
            ];
            for (let i = 0; i < el_id_list.length; i++) {
                getEl(el_id_list[i]).addEventListener(
                    "click",
                    cardRatingClickHandler,
                );
            }
        })();

        this._toggle_card(false);
        getEl("#show-fb-card").addEventListener("click", () => {
            this._toggle_card(true);
        });

        getEl("#card-back-image").addEventListener("click", function () {
            getEl("#zoomed-image-modal").style.display = "block";
        });
    }

    fill_queue(card_list) {
        card_list.forEach((card) => {
            this.cards.insert(card, QueueRank.Good);
        });
    }

    show_card() {
        if (!this.cards.isEmpty()) {
            const card = this.cards.next();
            this.currentCard = card;
            this._fill_template();
        } else {
            getEl("#study-deck-modal-content").innerHTML = "<p>Empty</p>";
        }
        return;
    }

    _fill_template() {
        getEl("#show-f-text").innerHTML = this.currentCard.card.front;
        getEl("#card-front").innerHTML = this.currentCard.card.front;
        getEl("#card-back").innerHTML = this.currentCard.card.back;
        if (this.currentCard.card.image_path) {
            getEl("#card-back-image").setAttribute(
                "src",
                this.currentCard.card.image_path,
            );
            getEl("#zoomed-image").setAttribute(
                "src",
                this.currentCard.card.image_path,
            );

            add_remove_html_class(
                getEl("#card-back-image"),
                "d-flex",
                "d-none",
            );
        } else {
            add_remove_html_class(
                getEl("#card-back-image"),
                "d-none",
                "d-flex",
            );
        }

        this._toggle_card(false);
    }

    _toggle_card(show_back) {
        if (show_back) {
            getEl("#show-fb-card").style.display = "none";

            add_remove_html_class(getEl("#fb-card"), "d-flex", "d-none");
        } else {
            getEl("#show-fb-card").style.display = "block";
            add_remove_html_class(getEl("#fb-card"), "d-none", "d-flex");
        }
    }
}
