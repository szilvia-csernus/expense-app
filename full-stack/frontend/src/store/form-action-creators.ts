import Cookies from 'js-cookie';
import { errorMessageActions } from './error-message-slice';
import { thankYouMessageActions } from './thank-you-message-slice';
import { costFormActions } from './cost-form-slice';
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

export const send = async (
	dispatch: Dispatch,
	formData: FormData,
	resetForm: () => void,
	resetFileUploader: () => void
) => {
	dispatch(costFormActions.setSending());
	const csrftoken = Cookies.get('csrftoken') || '';
	const result = await fetch(`/api/claims/send_expense_form/`, {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
		},
		body: formData,
	}).then(
		(response) => {
			if (response.status === 200) {
				dispatch(costFormActions.resetSending());
				dispatch(thankYouMessageActions.open());
				closeAfterTimeout(dispatch);
				resetForm();
			} else if (response.status === 406) {
				dispatch(costFormActions.resetSending());
				dispatch(
					errorMessageActions.setMessage(
						"Unfortunately, we were unable to process the file(s) you've uploaded. Please try another file format!"
					)
				);
				dispatch(errorMessageActions.open());
				// closeAfterTimeout(dispatch);
				resetFileUploader();
			} else {
				dispatch(costFormActions.resetSending());
				dispatch(
					errorMessageActions.setMessage(
						`An unknown error occured, apologies for the inconvenience!`
					)
				);
				dispatch(errorMessageActions.open());
				// closeAfterTimeout(dispatch);
			}
		},
		() => {
			dispatch(costFormActions.resetSending());
			dispatch(
				errorMessageActions.setMessage(
					`An Unknown error occured, apologies for the inconvenience!`
				)
			);
			dispatch(errorMessageActions.open());
			// closeAfterTimeout(dispatch);
		}
	);
	return result;
};
