export const reservedFieldNames = ["data", "initial", "only", "populate", "processing", "is_dirty", "reset", "withData"];

export function guardAgainstReservedFieldName(fieldName) {
	if (reservedFieldNames.indexOf(fieldName) !== -1) {
		throw new Error(`Field name ${fieldName} isn't allowed to be used in a Form or Errors instance.`);
	}
}

export function isArray(object) {
	return Object.prototype.toString.call(object) === "[object Array]";
}

export function merge(a, b) {
	for (const key in b) {
		a[key] = cloneDeep(b[key]);
	}
}

export function cloneDeep(object) {
	if (object === null) {
		return null;
	}

	if (Array.isArray(object)) {
		const clone = [];

		for (const key in object) {
			if (object.hasOwnProperty(key)) {
				clone[key] = cloneDeep(object[key]);
			}
		}

		return clone;
	}

	if (typeof object === "object") {
		const clone = {};

		for (const key in object) {
			if (object.hasOwnProperty(key)) {
				clone[key] = cloneDeep(object[key]);
			}
		}

		return clone;
	}

	return object;
}
