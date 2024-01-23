import { Dispatch } from '@reduxjs/toolkit';
import { churchActions } from './church-slice';

const djangoHost = import.meta.env.VITE_DJANGO_HOST;
const djangoPort = import.meta.env.VITE_DJANGO_PORT;
const host_url = `${djangoHost}:${djangoPort}`;

export const getChurchDetails = (dispatch: Dispatch, church: string) => {
	dispatch(churchActions.setFetchingInProcess(true));
	const fetchData = async () => {
		const response = await fetch(
			`${host_url}/churches/details/?church=${church}`
		);
		const data = await response.json();
		const { logo, cost_purposes } = data;
        if (response.status !== 200) {
            dispatch(churchActions.resetChurch())
        } else {
            dispatch(churchActions.setChurchDetails({ logo, cost_purposes }));
        }
		dispatch(churchActions.setFetchingInProcess(false));
	};
	return fetchData();
};

export const getChurches = (dispatch: Dispatch) => {
	dispatch(churchActions.setFetchingInProcess(true));
	const fetchData = async () => {
		const response = await fetch(`${host_url}/churches/names/`);
		const data = await response.json();
		const churchList = data.map((church: { name: string }) => church.name);
		dispatch(churchActions.setChurches(churchList));
	};
	return fetchData();
};