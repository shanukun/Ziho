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
    constructor() {
        this.cards = new CardQueue();
        this.scheduler = new Scheduler();
        this.currentCard = undefined;

        this._init_template();
    }

    _init_template() {
        const temp_html = getEl("#study-deck-template").content.cloneNode(true);

        getEl("#study-deck-modal-content").innerHTML = "";
        getEl("#study-deck-modal-content").appendChild(temp_html);

        const cardRatingClickHandler = (e) => {
            getEl("#show-ans-table").style.display = "block";
            getEl("#record-resp-table").style.display = "none";

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

        getEl("#show-ans-card").addEventListener("click", () => {
            getEl("#show-ans-table").style.display = "none";
            getEl("#record-resp-table").style.display = "block";
            getEl("#card-back").style.visibility = "visible";
        });
    }

    fill_queue(card_list) {
        card_list.forEach((card) => {
            this.cards.insert(card, Rating.Good);
        });
    }

    show_card() {
        if (!this.cards.isEmpty()) {
            const card = this.cards.next();
            this.currentCard = card;
            this._fill_template(card);
        } else {
            getEl("#study-deck-modal-content").innerHTML = "<p>Empty</p>";
        }
        return;
    }

    _fill_template(card) {
        getEl("#card-front").innerHTML = card.front;
        getEl("#card-back").innerHTML = card.back;

        getEl("#record-resp-table").style.display = "none";
        getEl("#card-back").style.visibility = "hidden";
    }
}

