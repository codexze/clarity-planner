import { guardAgainstReservedFieldName, isArray, merge } from "./helpers";
import equal from "deep-equal";

class Form {
	/**
	 * Create a new Form instance.
	 *
	 * @param {object} data
	 * @param {object} options
	 */
	constructor(data = {}, options = {}) {
		this.processing = false;

		this.withData(data);
	}

	withData(data) {
		if (isArray(data)) {
			data = data.reduce((carry, element) => {
				carry[element] = "";
				return carry;
			}, {});
		}

		this.setInitialValues(data);

		this.processing = false;

		for (const field in data) {
			guardAgainstReservedFieldName(field);

			this[field] = data[field];
		}

		return this;
	}

	/**
	 * Fetch all relevant data for the form.
	 */
	data() {
		const data = {};

		for (const property in this.initial) {
			data[property] = this[property];
		}

		return data;
	}

	/**
	 * Check if the form has changed.
	 *
	 * @return {boolean}
	 */
	dirty() {
		for (const property in this.initial) {
			if (!equal(this.initial[property], this[property])) {
				return true;
			}
		}

		return false;
	}

	/**
	 * Fetch all relevant data for the form and convert it to a formdata object.
	 */
	formData() {
		return this.data();
	}

	/**
	 * Fetch specific data for the form.
	 *
	 * @param {array} fields
	 * @return {object}
	 */
	only(fields) {
		return fields.reduce((filtered, field) => {
			filtered[field] = this[field];
			return filtered;
		}, {});
	}

	/**
	 * Reset the form fields.
	 */
	reset() {
		merge(this, this.initial);
	}

	setInitialValues(values) {
		this.initial = {};

		merge(this.initial, values);
	}

	populate(data) {
		Object.keys(data).forEach((field) => {
			guardAgainstReservedFieldName(field);

			if (this.hasOwnProperty(field)) {
				merge(this, { [field]: data[field] });
			}
		});

		return this;
	}

	static create(data = {}) {
		return new Form().withData(data);
	}
}

export default Form;
