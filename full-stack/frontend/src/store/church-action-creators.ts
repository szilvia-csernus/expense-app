import { Dispatch } from '@reduxjs/toolkit';
import { churchActions } from './church-slice';


export const getChurchDetails = (dispatch: Dispatch, church: string) => {
	dispatch(churchActions.setFetchingDetailsInProcess(true));
	const fetchData = async () => {
		const response = await fetch(
			`/api/churches/details/?church=${church}`
		);
		const data = await response.json();
		const { logo, cost_purposes } = data;
        if (response.status !== 200) {
            dispatch(churchActions.resetChurch())
        } else {
					dispatch(churchActions.setChurchDetails({ logo, cost_purposes }));
					
					// Pre-fetch and cache the logo image before the form gets rendered. While
					// fetchingInProcess is true, the loader is active on the form.
					const img = new Image();
					img.src = logo;
					img.onload = () => {
						dispatch(churchActions.setFetchingDetailsInProcess(false));
					};
				}
	};
	return fetchData();
};

export const getChurches = (dispatch: Dispatch) => {
	dispatch(churchActions.setFetchingChurchesInProcess(true));
	const fetchData = async () => {
		const response = await fetch(`/api/churches/names/`);
		const data = await response.json();
		const churchList = data.map((church: { short_name: string }) => church.short_name);
		dispatch(churchActions.setChurches(churchList));
		dispatch(churchActions.setFetchingChurchesInProcess(false));
	};
	return fetchData();
};