import { createSlice } from '@reduxjs/toolkit';

const errorMessageSlice = createSlice({
	name: 'errorMessage',
	initialState: {
		status: false,
		title: '',
		message: ''
	},
	reducers: {
		open(state) {
			state.status = true;
		},
		close(state) {
			state.status = false;
		},
		setMessage(state, action) {
			state.title = action.payload.title;
			state.message = action.payload.message;
		},
		resetMessage(state) {
			state.title = '';
			state.message = '';
		}
	},
});

export const errorMessageActions = errorMessageSlice.actions;

export default errorMessageSlice;