module.exports = {
  apps: [
    {
      name: "api-bot-austin",
      script: "./venv/bin/uvicorn",
      args: "main:app --reload --host 0.0.0.0 --port 8000",
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
