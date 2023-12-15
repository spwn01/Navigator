const { Client, Message } = require("@yuva1422/telegram.js");
const client = new Client();

const { config } = require("../util/constants");
const { token } = config;

client.on("ready", () => {
  console.log(client.user.firstName + " ready! ✅");
});

/**
 * @param {Message} message
 */
client.on("message", (message) => {
  console.log(message.content);
});

client.login(token);
client.startPolling();
