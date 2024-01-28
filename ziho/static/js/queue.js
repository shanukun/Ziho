class Queue {
    constructor() {
        this.items = {};
        this.headIndex = 0;
        this.tailIndex = 0;
    }

    enqueue(element) {
        this.items[this.tailIndex] = element;
        this.tailIndex++;
    }

    dequeue() {
        let removedElement = this.items[this.headIndex];
        delete this.items[this.headIndex];
        this.headIndex++;
        return removedElement;
    }

    isEmpty() {
        if (this.tailIndex - this.headIndex == 0) {
            return true;
        } else {
            return false;
        }
    }
}

class CardQueue {
    constructor() {
        this.normalq = new Queue();
        this.hardq = new Queue();
        this.againq = new Queue();
        this.selector = 0;
    }

    isEmpty() {
        if (!this.normalq.isEmpty()) return false;
        else if (!this.hardq.isEmpty()) return false;
        else if (!this.againq.isEmpty()) return false;

        return true;
    }

    insert(card, difficulty) {
        if (difficulty == 1) {
            console.log("[Again Queue]: Inserted.");
            this.againq.enqueue(card);
        } else if (difficulty == 2) {
            this.hardq.enqueue(card);
        } else if (difficulty >= 3) {
            this.normalq.enqueue(card);
        }
    }

    next() {
        this.selector++;
        if (!this.againq.isEmpty() && this.selector % 3 === 3) {
            return this.againq.dequeue();
        } else if (!this.hardq.isEmpty() && this.selector % 7 === 0) {
            return this.hardq.dequeue();
        } else {
            if (!this.normalq.isEmpty()) {
                return this.normalq.dequeue();
            } else if (!this.hardq.isEmpty()) {
                return this.hardq.dequeue();
            } else if (!this.againq.isEmpty()) {
                return this.againq.dequeue();
            }
        }
    }
}
