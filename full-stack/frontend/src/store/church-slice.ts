import { createSlice } from '@reduxjs/toolkit';

function getInitialChurch() {
	const params = new URLSearchParams(window.location.search);
	const adm = params.get('adm');
	const localChurch = localStorage.getItem('church') || '';
	return adm !== null ? adm : localChurch;
}

const initialChurch = getInitialChurch();

// Returns false if no church was selected and neither was a church present in the url 
const initialStatus =
	initialChurch === null || initialChurch === '';

const churchSlice = createSlice({
	name: 'church',
	initialState: {
		churches: [] as string[],
		status: initialStatus,
		church: initialChurch,
		fetchingDetailsInProcess: false,
		fetchingChurchesInProcess: false,
		logo: '',
		costPurposes: [] as { name: string; cost_code: number }[],
	},
	reducers: {
		open(state) {
			state.status = true;
		},
		close(state) {
			state.status = false;
		},
		setChurch(state, action) {
			state.church = action.payload;
			localStorage.setItem('church', action.payload);
		},
		resetChurch(state) {
			state.status = true;
			state.church = '';
			localStorage.removeItem('church');
		},
		setFetchingDetailsInProcess(state, action) {
			state.fetchingDetailsInProcess = action.payload;
		},
		setChurchDetails(state, action) {
			state.logo = action.payload['logo'];
			state.costPurposes = action.payload['cost_purposes'];
		},
		setChurches(state, action) {
			state.churches = action.payload;
		},
		setFetchingChurchesInProcess(state, action) {
			state.fetchingChurchesInProcess = action.payload;
		}
	},
});


export const churchActions = churchSlice.actions;

export default churchSlice;
