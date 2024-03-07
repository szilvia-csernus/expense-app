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
					errorMessageActions.setMessage({
						title: "ERROR",
						message: "Unfortunately, we were unable to process the file(s) you've uploaded. Please try another file format!"
					})
						
				);
				dispatch(errorMessageActions.open());
				// closeAfterTimeout(dispatch);
				resetFileUploader();
			} else if (response.status === 400 || response.status === 404 || response.status === 500) {
				dispatch(costFormActions.resetSending());
				dispatch(
					errorMessageActions.setMessage(
						{
							title: 'ERROR',
							message:
								`An unknown error occured, apologies for the inconvenience!`
						})
				);
				dispatch(errorMessageActions.open());
				// closeAfterTimeout(dispatch);
			} else {
				dispatch(costFormActions.resetSending());
				dispatch(
					errorMessageActions.setMessage({
						title: 'ERROR',
						message: `An unknown error occured, apologies for the inconvenience!`,
					})
				);
				dispatch(errorMessageActions.open());
			}
		},
		() => {
			dispatch(costFormActions.resetSending());
			dispatch(
				errorMessageActions.setMessage({
					title: 'OFFLINE',
					message: `It seems you're currently offline. We will try to send your 
					form in the next 48 hours if your network recovers. 
					If you don't get a confirmation email during this period, 
					please try submitting your form again.`,
				})
			);
			dispatch(errorMessageActions.open());
			// closeAfterTimeout(dispatch);
			resetForm();
		}
	);
	return result;
};
