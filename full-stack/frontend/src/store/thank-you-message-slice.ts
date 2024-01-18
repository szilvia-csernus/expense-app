import { createSlice } from '@reduxjs/toolkit';

const thankYouMessageSlice = createSlice({
	name: 'thankYouMessage',
	initialState: false,
	reducers: {
		open() {
			return true;
		},
		close() {
			return false;
		},
	},
});

export const thankYouMessageActions = thankYouMessageSlice.actions;

export default thankYouMessageSlice;
