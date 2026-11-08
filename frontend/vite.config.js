import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { loadEnv } from 'vite';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));

export default defineConfig(({ mode }) => {
  const { API_PORT = '8000' } = loadEnv(mode, root, 'API_PORT');
  const port = Number(API_PORT || '8000');
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error('API_PORT debe ser un puerto entero entre 1 y 65535.');
  }

  return {
    plugins: [react()],
    server: {
      host: '127.0.0.1', port: 5173, strictPort: true,
      proxy: { '/api': { target: `http://127.0.0.1:${port}`, changeOrigin: false, rewrite: path => path.replace(/^\/api/, '') } },
    },
    test: { maxWorkers: 2, environment: 'jsdom', setupFiles: ['./src/test-setup.js'], clearMocks: true },
  };
});
