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
			strategies: 'generateSW',
			registerType: 'autoUpdate',
			devOptions: {
				enabled: true,
			},
			workbox: {
				globPatterns: ['**/*.{js,jsx,ts,tsx,css,html,ico,png,webmanifest}'],
				runtimeCaching: [
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
						urlPattern: /^https?:\/\//i,
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
				],
			},
			manifest: {
				id: 'expense-app',
				short_name: 'Expense App',
				name: 'Expense App for Redeemer Churches',
				description:
					'Expense Reimbursement App for Redeemer Churches in the Neatherlands',
				lang: 'en-US',
				theme_color: '#000000',
				icons: [
					{
						src: 'icon-36x36.png',
						type: 'image/png',
						sizes: '36x36',
						purpose: 'any',
					},
					{
						src: 'icon-48x48.png',
						type: 'image/png',
						sizes: '48x48',
						purpose: 'any',
					},
					{
						src: 'icon-72x72.png',
						type: 'image/png',
						sizes: '72x72',
						purpose: 'any',
					},
					{
						src: 'icon-96x96.png',
						type: 'image/png',
						sizes: '96x96',
						purpose: 'any',
					},
					{
						src: 'icon-144x144.png',
						type: 'image/png',
						sizes: '144x144',
						purpose: 'any',
					},
					{
						src: 'icon-192x192.png',
						type: 'image/png',
						sizes: '192x192',
						purpose: 'any',
					},
					{
						src: 'icon-512x512.png',
						type: 'image/png',
						sizes: '512x512',
						purpose: 'any',
					},
					{
						src: 'icon-square-180x180.png',
						type: 'image/png',
						sizes: '180x180',
						purpose: 'maskable',
					},
					{
						src: 'icon-square-180x180.png',
						type: 'image/png',
						sizes: '180x180',
						purpose: 'any',
					},
				],
				start_url: '/',
				scope: '/',
				display: 'standalone',
				orientation: 'portrait',
				background_color: '#232426',
				categories: ['finance'],
				launch_handler: {
					client_mode: ['navigate-existing', 'auto'],
				},
			},
		}),
	],
});
