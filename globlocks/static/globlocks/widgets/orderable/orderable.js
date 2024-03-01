class OrderableInput {
    constructor(querySelector, values) {

        let v;
        if (typeof values === 'string') {
            try {
                v = JSON.parse(values);
            } catch (e) {
                v = [];
            }
        } else {
            v = values;
        }

        this.element = document.querySelector("#"+querySelector);
        this.input = document.querySelector(`#${querySelector}-input`);
        this.setState(v);
        this.sortable = new Sortable(this.element, {
            animation: 150,
            onEnd: () => {
                this.input.value = JSON.stringify(this.values());
            }
        });
    }

    values() {
        let values = [];
        for (let i = 0; i < this.element.children.length; i++) {
            values.push(this.element.children[i].dataset.value);
        }
        return values;
    }

    setState(values) {
        let children = Array.from(this.element.children); // Convert NodeList to array

        // First, put the children in the same order as the values array
        let orderedChildren = [];

        if (values) {
            for (let value of values) {
                if (typeof value === 'object') {
                    value = value.value;
                }
                let matchingChild = children.find(child => child.dataset.value === value);
                if (matchingChild) {
                    orderedChildren.push(matchingChild);
                    children = children.filter(child => child !== matchingChild); // Remove added child from the list
                }
            }
        }


        // Then append any remaining children that were not in the values array
        orderedChildren = [...orderedChildren, ...children];

        this.element.innerHTML = '';
        for (let i = 0; i < orderedChildren.length; i++) {
            this.element.appendChild(orderedChildren[i]);
        }

        this.input.value = JSON.stringify(this.values());
    }

    getState() {
        return this.values();
    }

    getValue() {
        return this.input.value;
    }

    focus() {
        this.element.focus();
    }
}