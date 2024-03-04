import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import dotenv from 'dotenv';
import { VitePWA } from 'vite-plugin-pwa';

// Load environment variables
dotenv.config();

// https://vitejs.dev/config/
export default defineConfig({
	server: {
		proxy: {
			'/api': {
				target: 'http://127.0.0.1:8000',
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, ''),
			},
		},
	},
	plugins: [
		react(),
		VitePWA({
			manifest: false,
			strategies: 'generateSW',
			registerType: 'autoUpdate',
			devOptions: {
				enabled: true,
			},
			workbox: {
				globPatterns: ['**/*.{js,jsx,ts,tsx,css,html,ico,png}'],
				runtimeCaching: [
					{
						urlPattern: /^http:\/\/localhost/i,
						handler: 'CacheFirst',
						options: {
							cacheName: 'landing-page',
							expiration: {
								maxEntries: 1,
								maxAgeSeconds: 60 * 60 * 24 * 7, // 7 days
							},
							cacheableResponse: {
								statuses: [0, 200],
							},
						},
					},
					{
						urlPattern: /^https:\/\/res.cloudinary*/i,
						handler: 'CacheFirst',
						options: {
							cacheName: 'cost-center-logos',
							expiration: {
								maxEntries: 1,
								maxAgeSeconds: 60 * 60 * 24 * 7, // 7 days
							},
							cacheableResponse: {
								statuses: [0, 200],
							},
						},
					},
					{
						urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
						handler: 'CacheFirst',
						options: {
							cacheName: 'google-fonts-cache',
							expiration: {
								maxEntries: 10,
								maxAgeSeconds: 60 * 60 * 24 * 365, // <== 365 days
							},
							cacheableResponse: {
								statuses: [0, 200],
							},
						},
					},
					{
						urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
						handler: 'CacheFirst',
						options: {
							cacheName: 'gstatic-fonts-cache',
							expiration: {
								maxEntries: 10,
								maxAgeSeconds: 60 * 60 * 24 * 365, // <== 365 days
							},
							cacheableResponse: {
								statuses: [0, 200],
							},
						},
					},
					{
						urlPattern: /^https:\/\/www\.redeemerdelft\.nl\/.*/i,
						handler: 'CacheFirst',
						options: {
							cacheName: 'logo-cache',
							expiration: {
								maxEntries: 10,
								maxAgeSeconds: 60 * 60 * 24 * 365, // <== 365 days
							},
							cacheableResponse: {
								statuses: [0, 200],
							},
						},
					},
				],
			},
		}),
	],
});
