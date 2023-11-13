/*
 *
 * https://github.com/open-spaced-repetition/fsrs.js/blob/master/src/index.ts
 *
 */

var __assign =
    (this && this.__assign) ||
    function () {
        __assign =
            Object.assign ||
            function (t) {
                for (var s, i = 1, n = arguments.length; i < n; i++) {
                    s = arguments[i];
                    for (var p in s)
                        if (Object.prototype.hasOwnProperty.call(s, p))
                            t[p] = s[p];
                }
                return t;
            };
        return __assign.apply(this, arguments);
    };
var State;
(function (State) {
    State[(State["New"] = 0)] = "New";
    State[(State["Learning"] = 1)] = "Learning";
    State[(State["Review"] = 2)] = "Review";
    State[(State["Relearning"] = 3)] = "Relearning";
})(State || (State = {}));
var Rating;
(function (Rating) {
    Rating[(Rating["Again"] = 1)] = "Again";
    Rating[(Rating["Hard"] = 2)] = "Hard";
    Rating[(Rating["Good"] = 3)] = "Good";
    Rating[(Rating["Easy"] = 4)] = "Easy";
})(Rating || (Rating = {}));
var ReviewLog = /** @class */ (function () {
    function ReviewLog(rating, elapsed_days, scheduled_days, review, state) {
        this.rating = rating;
        this.elapsed_days = elapsed_days;
        this.scheduled_days = scheduled_days;
        this.review = review;
        this.state = state;
    }
    return ReviewLog;
})();
var Card = /** @class */ (function () {
    function Card(
        due,
        stability,
        difficulty,
        elapsed_days,
        scheduled_days,
        reps,
        lapses,
        state,
        last_review,
    ) {
        if (due === void 0) {
            due = new Date();
        }
        if (stability === void 0) {
            stability = 0;
        }
        if (difficulty === void 0) {
            difficulty = 0;
        }
        if (elapsed_days === void 0) {
            elapsed_days = 0;
        }
        if (scheduled_days === void 0) {
            scheduled_days = 0;
        }
        if (reps === void 0) {
            reps = 0;
        }
        if (lapses === void 0) {
            lapses = 0;
        }
        if (state === void 0) {
            state = State.New;
        }
        if (last_review === void 0) {
            last_review = new Date();
        }
        this.due = due;
        this.stability = stability;
        this.difficulty = difficulty;
        this.elapsed_days = elapsed_days;
        this.scheduled_days = scheduled_days;
        this.reps = reps;
        this.lapses = lapses;
        this.state = state;
        this.last_review = last_review;
    }
    return Card;
})();
var SchedulingInfo = /** @class */ (function () {
    function SchedulingInfo(card, review_log) {
        this.card = card;
        this.review_log = review_log;
    }
    return SchedulingInfo;
})();
var SchedulingCards = /** @class */ (function () {
    function SchedulingCards(card) {
        this.again = __assign({}, card);
        this.hard = __assign({}, card);
        this.good = __assign({}, card);
        this.easy = __assign({}, card);
    }
    SchedulingCards.prototype.update_state = function (state) {
        if (state === State.New) {
            this.again.state = State.Learning;
            this.hard.state = State.Learning;
            this.good.state = State.Learning;
            this.easy.state = State.Review;
            this.again.lapses += 1;
        } else if (state === State.Learning || state === State.Relearning) {
            this.again.state = state;
            this.hard.state = state;
            this.good.state = State.Review;
            this.easy.state = State.Review;
        } else if (state === State.Review) {
            this.again.state = State.Relearning;
            this.hard.state = State.Review;
            this.good.state = State.Review;
            this.easy.state = State.Review;
            this.again.lapses += 1;
        }
    };
    SchedulingCards.prototype.schedule = function (
        now,
        hard_interval,
        good_interval,
        easy_interval,
    ) {
        this.again.scheduled_days = 0;
        this.hard.scheduled_days = hard_interval;
        this.good.scheduled_days = good_interval;
        this.easy.scheduled_days = easy_interval;
        this.again.due = new Date(now.getTime() + 5 * 60 * 1000);
        if (hard_interval > 0) {
            this.hard.due = new Date(
                now.getTime() + hard_interval * 24 * 60 * 60 * 1000,
            );
        } else {
            this.hard.due = new Date(now.getTime() + 10 * 60 * 1000);
        }
        this.good.due = new Date(
            now.getTime() + good_interval * 24 * 60 * 60 * 1000,
        );
        this.easy.due = new Date(
            now.getTime() + easy_interval * 24 * 60 * 60 * 1000,
        );
    };
    SchedulingCards.prototype.record_log = function (card, now) {
        var _a;
        return (
            (_a = {}),
            (_a[Rating.Again] = new SchedulingInfo(
                this.again,
                new ReviewLog(
                    Rating.Again,
                    this.again.scheduled_days,
                    card.elapsed_days,
                    now,
                    card.state,
                ),
            )),
            (_a[Rating.Hard] = new SchedulingInfo(
                this.hard,
                new ReviewLog(
                    Rating.Hard,
                    this.hard.scheduled_days,
                    card.elapsed_days,
                    now,
                    card.state,
                ),
            )),
            (_a[Rating.Good] = new SchedulingInfo(
                this.good,
                new ReviewLog(
                    Rating.Good,
                    this.good.scheduled_days,
                    card.elapsed_days,
                    now,
                    card.state,
                ),
            )),
            (_a[Rating.Easy] = new SchedulingInfo(
                this.easy,
                new ReviewLog(
                    Rating.Easy,
                    this.easy.scheduled_days,
                    card.elapsed_days,
                    now,
                    card.state,
                ),
            )),
            _a
        );
    };
    return SchedulingCards;
})();
var Params = /** @class */ (function () {
    function Params() {
        this.request_retention = 0.9;
        this.maximum_interval = 36500;
        this.w = [
            0.4, 0.6, 2.4, 5.8, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14, 0.94, 2.18,
            0.05, 0.34, 1.26, 0.29, 2.61,
        ];
    }
    return Params;
})();
var FSRS = /** @class */ (function () {
    function FSRS() {
        this.p = new Params();
    }
    FSRS.prototype.repeat = function (card, now) {
        card = __assign({}, card);
        if (card.state === State.New) {
            card.elapsed_days = 0;
        } else {
            card.elapsed_days =
                (now.getTime() - card.last_review.getTime()) / 86400000;
        }
        card.last_review = now;
        card.reps += 1;
        var s = new SchedulingCards(card);
        s.update_state(card.state);
        if (card.state === State.New) {
            this.init_ds(s);
            s.again.due = new Date(now.getTime() + 60 * 1000);
            s.hard.due = new Date(now.getTime() + 5 * 60 * 1000);
            s.good.due = new Date(now.getTime() + 10 * 60 * 1000);
            var easy_interval = this.next_interval(s.easy.stability);
            s.easy.scheduled_days = easy_interval;
            s.easy.due = new Date(
                now.getTime() + easy_interval * 24 * 60 * 60 * 1000,
            );
        } else if (
            card.state === State.Learning ||
            card.state === State.Relearning
        ) {
            var hard_interval = 0;
            var good_interval = this.next_interval(s.good.stability);
            var easy_interval = Math.max(
                this.next_interval(s.easy.stability),
                good_interval + 1,
            );
            s.schedule(now, hard_interval, good_interval, easy_interval);
        } else if (card.state === State.Review) {
            var interval = card.elapsed_days;
            var last_d = card.difficulty;
            var last_s = card.stability;
            var retrievability = Math.pow(1 + interval / (9 * last_s), -1);
            this.next_ds(s, last_d, last_s, retrievability);
            var hard_interval = this.next_interval(s.hard.stability);
            var good_interval = this.next_interval(s.good.stability);
            hard_interval = Math.min(hard_interval, good_interval);
            good_interval = Math.max(good_interval, hard_interval + 1);
            var easy_interval = Math.max(
                this.next_interval(s.easy.stability),
                good_interval + 1,
            );
            s.schedule(now, hard_interval, good_interval, easy_interval);
        }
        return s.record_log(card, now);
    };
    FSRS.prototype.init_ds = function (s) {
        s.again.difficulty = this.init_difficulty(Rating.Again);
        s.again.stability = this.init_stability(Rating.Again);
        s.hard.difficulty = this.init_difficulty(Rating.Hard);
        s.hard.stability = this.init_stability(Rating.Hard);
        s.good.difficulty = this.init_difficulty(Rating.Good);
        s.good.stability = this.init_stability(Rating.Good);
        s.easy.difficulty = this.init_difficulty(Rating.Easy);
        s.easy.stability = this.init_stability(Rating.Easy);
    };
    FSRS.prototype.next_ds = function (s, last_d, last_s, retrievability) {
        s.again.difficulty = this.next_difficulty(last_d, Rating.Again);
        s.again.stability = this.next_forget_stability(
            s.again.difficulty,
            last_s,
            retrievability,
        );
        s.hard.difficulty = this.next_difficulty(last_d, Rating.Hard);
        s.hard.stability = this.next_recall_stability(
            s.hard.difficulty,
            last_s,
            retrievability,
            Rating.Hard,
        );
        s.good.difficulty = this.next_difficulty(last_d, Rating.Good);
        s.good.stability = this.next_recall_stability(
            s.good.difficulty,
            last_s,
            retrievability,
            Rating.Good,
        );
        s.easy.difficulty = this.next_difficulty(last_d, Rating.Easy);
        s.easy.stability = this.next_recall_stability(
            s.easy.difficulty,
            last_s,
            retrievability,
            Rating.Easy,
        );
    };
    FSRS.prototype.init_stability = function (r) {
        return Math.max(this.p.w[r - 1], 0.1);
    };
    FSRS.prototype.init_difficulty = function (r) {
        return Math.min(Math.max(this.p.w[4] - this.p.w[5] * (r - 3), 1), 10);
    };
    FSRS.prototype.next_interval = function (s) {
        var interval = s * 9 * (1 / this.p.request_retention - 1);
        return Math.min(
            Math.max(Math.round(interval), 1),
            this.p.maximum_interval,
        );
    };
    FSRS.prototype.next_difficulty = function (d, r) {
        var next_d = d - this.p.w[6] * (r - 3);
        return Math.min(
            Math.max(this.mean_reversion(this.p.w[4], next_d), 1),
            10,
        );
    };
    FSRS.prototype.mean_reversion = function (init, current) {
        return this.p.w[7] * init + (1 - this.p.w[7]) * current;
    };
    FSRS.prototype.next_recall_stability = function (d, s, r, rating) {
        var hard_penalty = rating === Rating.Hard ? this.p.w[15] : 1;
        var easy_bonus = rating === Rating.Easy ? this.p.w[16] : 1;
        return (
            s *
            (1 +
                Math.exp(this.p.w[8]) *
                    (11 - d) *
                    Math.pow(s, -this.p.w[9]) *
                    (Math.exp((1 - r) * this.p.w[10]) - 1) *
                    hard_penalty *
                    easy_bonus)
        );
    };
    FSRS.prototype.next_forget_stability = function (d, s, r) {
        return (
            this.p.w[11] *
            Math.pow(d, -this.p.w[12]) *
            (Math.pow(s + 1, this.p.w[13]) - 1) *
            Math.exp((1 - r) * this.p.w[14])
        );
    };
    return FSRS;
})();
