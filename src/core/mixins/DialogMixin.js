export default {
	methods: {
		toast(title, message, variant, sticky = false, delay = 1000, hideCloseButton = true) {
			this.$bvToast.toast(message, {
				solid: true,
				title: title,
				variant: variant,
				noAutoHide: sticky,
				autoHideDelay: delay,
				noCloseButton: hideCloseButton,
			})
		},
		dialog(title, message, okTitle = "Confirm", cancelTitle = "Cancel", okVariant = "danger") {
			return this.$bvModal
			.msgBoxConfirm(message, {
				title: title,
				size: "md",
				buttonSize: "lg",
				okVariant: "danger",
				okTitle: okTitle,
				cancelTitle: cancelTitle,
				footerClass: "p-2",
				hideHeaderClose: false,
				centered: true,
			})
			.then((value) => {
				return value
			})
			.catch((err) => {
				// An error occurred
			})
		}
	}
}
