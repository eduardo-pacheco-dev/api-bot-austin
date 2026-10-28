module.exports = {
  apps: [
    {
      name: "api-bot-austin-telegram",
      script: "./venv/bin/python",
      args: "bot.py",
      interpreter: "none",
      env: {
        NODE_ENV: "development",
      },
      env_production: {
        NODE_ENV: "production",
      },
      autorestart: true,
      watch: false,
    },
  ],
};
