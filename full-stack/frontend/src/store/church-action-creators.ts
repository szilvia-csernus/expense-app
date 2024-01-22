import { Dispatch } from '@reduxjs/toolkit';
import { selectChurchActions } from './select-church-slice';

export const getChurchDetails = (dispatch: Dispatch, church: string) => {
	dispatch(selectChurchActions.setFetchingInProcess(true));
	const fetchData = async () => {
		const response = await fetch(
			`http://localhost:8000/churches/purposes/?church=${church}`
		);
		const data = await response.json();
		const { logo, cost_purposes } = data;
		dispatch(selectChurchActions.setChurchDetails({ logo, cost_purposes }));
		dispatch(selectChurchActions.setFetchingInProcess(false));
	};
	return fetchData();
};