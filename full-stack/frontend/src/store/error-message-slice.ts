import { createSlice } from '@reduxjs/toolkit';

const errorMessageSlice = createSlice({
	name: 'errorMessage',
	initialState: {
		status: false,
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
			state.message = action.payload
		},
		resetMessage(state) {
			state.message = ''
		}
	},
});

export const errorMessageActions = errorMessageSlice.actions;

export default errorMessageSlice;