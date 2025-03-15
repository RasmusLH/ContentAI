const path = require('path');

module.exports = {
  // ...existing code...
  
  devServer: {
    static: {
      directory: path.join(__dirname, 'public'),
    },
    setupMiddlewares: (middlewares, devServer) => {
      if (!devServer) {
        throw new Error('webpack-dev-server is not defined');
      }

      // Add your before setup middleware here if needed
      // devServer.app.get('/some-route', (req, res) => { ... });

      return middlewares;
    },
    compress: true,
    port: 3000,
    hot: true,
    // Remove deprecated options if they exist
    // onBeforeSetupMiddleware: null,
    // onAfterSetupMiddleware: null,
  },
  // ...existing code...
};