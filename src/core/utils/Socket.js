// socketPlugin.js
export const Socket = {
	install(app) {
		app.config.globalProperties.$websocket = {
			socket: null,
			isConnected: false,
			connectionAttempts: 0,
			maxConnectionAttempts: 5,
			retryDelay: 3000,

			isSSL() {
				return window.location.protocol === "https:";
			},

			handleMessage(event) {
				const message = event.data;
				this.$emit("messageReceived", message); // you might need an emitter or custom event for this
			},

			connect(url) {
				const wUrl = this.isSSL() ? `wss://${url}` : `ws://${url}`;
				this.socket = new WebSocket(wUrl);

				this.socket.addEventListener("open", () => {
					this.isConnected = true;
					this.connectionAttempts = 0;
					console.log("WebSocket connected");
				});

				this.socket.addEventListener("message", this.handleMessage);

				this.socket.addEventListener("close", (event) => {
					this.isConnected = false;
					console.log("WebSocket disconnected");

					if (event.code !== 1000 && event.code !== 1005) {
						if (this.connectionAttempts < this.maxConnectionAttempts) {
							setTimeout(() => {
								this.connectionAttempts++;
								console.log("Retry connecting...");
								this.connect(url);
							}, this.retryDelay);
						} else {
							console.log("Exceeded maximum connection attempts, disconnecting...");
							this.disconnect();
						}
					}
				});
			},

			send(message) {
				if (this.isConnected) {
					this.socket.send(message);
				} else {
					console.log("WebSocket is not connected");
				}
			},

			disconnect() {
				if (this.isConnected) {
					this.socket.close();
					this.socket.removeEventListener("message", this.handleMessage);
					this.socket.removeEventListener("close", {});
					this.socket.removeEventListener("open", {});
					this.socket = null;
					this.isConnected = false;
					console.log("WebSocket disconnected");
				} else {
					console.log("WebSocket is not connected");
				}
			},
		};
	},
};
