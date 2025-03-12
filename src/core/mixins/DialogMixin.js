import { useToast } from "vue-toastification";

export default {
	data() {
		return {};
	},
	methods: {
		toastError(message, timeout = 5000) {
			const toast = useToast();
			toast.error(message, {
				position: "bottom-center",
				timeout: timeout,
				closeOnClick: false,
				pauseOnFocusLoss: true,
				pauseOnHover: true,
				draggable: true,
				draggablePercent: 0.6,
				showCloseButtonOnHover: true,
				hideProgressBar: true,
				closeButton: "button",
				icon: true,
				rtl: false,
			});
		},
		toastWarning(message, timeout = 5000) {
			const toast = useToast();
			toast.warning(message, {
				position: "bottom-center",
				timeout: timeout,
				closeOnClick: false,
				pauseOnFocusLoss: true,
				pauseOnHover: true,
				draggable: true,
				draggablePercent: 0.6,
				showCloseButtonOnHover: true,
				hideProgressBar: true,
				closeButton: "button",
				icon: true,
				rtl: false,
			});
		},
		toastSuccess(message, timeout = 5000) {
			const toast = useToast();
			toast.success(message, {
				position: "bottom-center",
				timeout: timeout,
				closeOnClick: false,
				pauseOnFocusLoss: true,
				pauseOnHover: true,
				draggable: true,
				draggablePercent: 0.6,
				showCloseButtonOnHover: true,
				hideProgressBar: true,
				closeButton: "button",
				icon: true,
				rtl: false,
			});
		},
		toastInfo(message, timeout = 5000) {
			const toast = useToast();
			toast.info(message, {
				position: "bottom-center",
				timeout: timeout,
				closeOnClick: false,
				pauseOnFocusLoss: true,
				pauseOnHover: true,
				draggable: true,
				draggablePercent: 0.6,
				showCloseButtonOnHover: true,
				hideProgressBar: true,
				closeButton: "button",
				icon: true,
				rtl: false,
			});
		},
		toastComponent(component, timeout = false, options = {}) {
			const toast = useToast();
			toast(component, { timeout: timeout, ...options });
		},
	},
};
