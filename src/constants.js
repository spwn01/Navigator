require("dotenv").config();

const config = {
  token: process.env.TOKEN,
  mongo: "waw",
};

module.exports.config = config;
