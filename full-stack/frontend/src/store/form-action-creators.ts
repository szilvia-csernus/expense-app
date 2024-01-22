import { errorMessageActions } from './error-message-slice';
import { thankYouMessageActions } from './thank-you-message-slice';
import { costFormActions } from './cost-form-slice';
import rotterdamLogoUrl from '../images/rotterdamLogo.png';
import delftLogoUrl from '../images/delftLogo.png';
import { AppDispatch } from '.';
import { Dispatch } from '@reduxjs/toolkit';

function closeAfterTimeout(dispatch: AppDispatch) {
	const timeoutId = setTimeout(() => {
		dispatch(errorMessageActions.close());
		dispatch(thankYouMessageActions.close());
		dispatch(errorMessageActions.resetMessage());
	}, 10000);

	return () => clearTimeout(timeoutId);
}

const fetchAndAppendChurchLogo = async (formData: FormData) => {
	const church = formData.get('church');
	if (church === 'Rotterdam') {
		return fetch(rotterdamLogoUrl)
			.then((response) => response.blob())
			.then((blob) => {
				formData.append('logo', blob, 'logo.png');
			});
	} else if (church === 'Delft') {
		return fetch(delftLogoUrl)
			.then((response) => response.blob())
			.then((blob) => {
				formData.append('logo', blob, 'logo.png');
			});
	}
};

export const send = async (
	dispatch: Dispatch,
	formData: FormData,
	resetForm: () => void,
	resetFileUploader: () => void
) => {
	dispatch(costFormActions.setSending());

	await fetchAndAppendChurchLogo(formData);

	const result = await fetch(
		'http://127.0.0.1:8000/claims/send_expense_form/',
		{
			method: 'POST',
			body: formData,
		}
	).then(
		(response) => {
			if (response.status === 200) {
				dispatch(costFormActions.resetSending());
				dispatch(thankYouMessageActions.open());
				closeAfterTimeout(dispatch);
				resetForm();
			} else if (response.status === 422) {
				dispatch(costFormActions.resetSending());
				dispatch(
					errorMessageActions.setMessage(
						'Oops! We couldn’t open this PDF file, please make a screenshot or a photo instead! Thanks!'
					)
				);
				dispatch(errorMessageActions.open());
				// closeAfterTimeout(dispatch);
				resetFileUploader();
			} else {
				dispatch(costFormActions.resetSending());
				dispatch(
					errorMessageActions.setMessage(
						`An unknown error occured, apologies for the inconvenience! ${response.status}`
					)
				);
				dispatch(errorMessageActions.open());
				// closeAfterTimeout(dispatch);
			}
		},
		(error) => {
			dispatch(costFormActions.resetSending());
			dispatch(
				errorMessageActions.setMessage(
					`An Unknown error occured, apologies for the inconvenience! ${error}`
				)
			);
			dispatch(errorMessageActions.open());
			// closeAfterTimeout(dispatch);
		}
	);
	return result;
};
