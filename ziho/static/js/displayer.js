class Scheduler {
    constructor() {
        this.f = new FSRS();
    }

    isGraduated(card, rating) {
        const s_card = this.f.repeat(card, new Date())[rating].card;
        // console.log(s_card.due);

        let queue_rating = Rating.Good;
        if (s_card.due < new Date(Date.now() + 5 * 60 * 1000)) {
            queue_rating = Rating.Again;
        } else if (s_card.due < new Date(Date.now() + 10 * 60 * 1000)) {
            queue_rating = Rating.Hard;
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
            const card_status = this.scheduler.isGraduated(
                Scheduler.toCard(this.currentCard.card_info),
                card_rating,
            );

            if (card_status.graduated) {
                this.currentCard.card_info = card_status.card_info;
                save_card(this.currentCard);
            } else {
                this.currentCard.card_info = card_status.card_info;
                this.cards.insert(this.currentCard, card_status.queue);
            }

            this.show_card();
            return;
        };

        getEl("#again-card").addEventListener("click", cardRatingClickHandler);
        getEl("#hard-card").addEventListener("click", cardRatingClickHandler);
        getEl("#good-card").addEventListener("click", cardRatingClickHandler);
        getEl("#easy-card").addEventListener("click", cardRatingClickHandler);

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
            // Rating.Good for normal queue
            this.cards.insert(card, Rating.Good);
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
        getEl("#show-f-text").innerHTML = this.currentCard.front;
        getEl("#card-front").innerHTML = this.currentCard.front;
        getEl("#card-back").innerHTML = this.currentCard.back;
        if (this.currentCard.image_path) {
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

            getEl("#card-back-image").classList.add("d-flex");
            getEl("#card-back-image").classList.remove("d-none");
        } else {
            getEl("#card-back-image").classList.remove("d-flex");
            getEl("#card-back-image").classList.add("d-none");
        }

        this._toggle_card(false);
    }

    _toggle_card(back) {
        if (back) {
            getEl("#show-fb-card").style.display = "none";
            getEl("#fb-card").classList.remove("d-none");
            getEl("#fb-card").classList.add("d-flex");
        } else {
            getEl("#show-fb-card").style.display = "block";
            getEl("#fb-card").classList.remove("d-flex");
            getEl("#fb-card").classList.add("d-none");
        }
    }
}
