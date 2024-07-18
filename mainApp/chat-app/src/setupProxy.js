const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/send_message",
    createProxyMiddleware({
      target: "https://faf3-34-16-150-3.ngrok-free.app",
      changeOrigin: true,
      secure: false, // Bypasses SSL verification
      onProxyReq: (proxyReq, req, res) => {
        proxyReq.setHeader("Origin", "https://faf3-34-16-150-3.ngrok-free.app");
      },
    })
  );
};
