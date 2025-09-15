import moment from "moment";

export default {
	data() {
		return {
			currentDateTime: null,
		};
	},
	computed: {
		getWeekdays() {
			// console.log(moment.weekdays().map(w => w))
			// const days = moment.weekdays().map((v,i) => [String(i),v])
			// console.log(days)

			return moment.weekdays();
		},
	},
	methods: {
		toFullDate(date) {
			return moment(date).locale("en").format("ddd DD MMMM YYYY");
		},
		toLocaleDate(date) {
			return moment.tz(date, "America/Paramaribo").locale("en").format("DD MMM YYYY");
		},
		toLocaleDateTime(datetime) {
			return moment.tz(datetime, "America/Paramaribo").locale("en").format("DD MMM YYYY HH:mm");
		},
		toLocaleTimeFromDateTime(datetime) {
			return moment.tz(datetime, "America/Paramaribo").locale("en").format("HH:mm");
		},
		toLocaleTime(time) {
			return moment.tz(time, "HH:mm:ss", "America/Paramaribo").locale("en").format("HH:mm");
		},
		dateToLocaleTime(date) {
			return moment.tz(date, "America/Paramaribo").locale("en").format("HH:mm");
		},
		toWeekday(date) {
			return moment(date).locale("en").format("dddd");
		},
		toAgo(datetime) {
			return moment(datetime).locale("en").fromNow();
		},
		dynamicDateTime(datetime) {
			var now = moment();
			if (moment(datetime).year() === now.year()) {
				if (moment(datetime).day() === now.day()) {
					return this.toLocaleTimeFromDateTime(datetime);
				}

				return moment(datetime).locale("en").format("DD MMM");
			}

			return this.toLocaleDate(datetime);
		},
		timeNow() {
			var now = moment();
			return this.dateToLocaleTime(now);
		},
		dateTimeNow() {
			var now = moment();
			return this.toLocaleDateTime(now);
		},
	},
	mounted() {
		//short ago
		moment.updateLocale("en", {
			week: {
				dow: 1, // First day of week is Monday
			},
			relativeTime: {
				future: "in %s",
				past: "%s ago",
				s: "seconds",
				ss: "%ss",
				m: "a minute",
				mm: "%dm",
				h: "an hour",
				hh: "%dh",
				d: "a day",
				dd: "%dd",
				M: "a month",
				MM: "%dM",
				y: "a year",
				yy: "%dY",
			},
		});

		moment.updateLocale("nl", {
			week: {
				dow: 1, // First day of week is Monday
			},
			relativeTime: {
				future: "in %s",
				past: "%s geleden",
				s: "paar seconden",
				ss: "%ss",
				m: "minuut",
				mm: "%dm",
				h: "uur",
				hh: "%dh",
				d: "dag",
				dd: "%dd",
				M: "maand",
				MM: "%dM",
				y: "jaar",
				yy: "%dY",
			},
		});

		setInterval(() => {
			this.currentDateTime = this.dateTimeNow();
		}, 1000);
	},
};
