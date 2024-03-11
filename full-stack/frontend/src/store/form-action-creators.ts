import Cookies from 'js-cookie';
import { errorMessageActions } from './error-message-slice';
import { thankYouMessageActions } from './thank-you-message-slice';
import { costFormActions } from './cost-form-slice';
import { AppDispatch } from '.';
import { Action, Dispatch } from '@reduxjs/toolkit';

/** Dispatch the callback function after 10s delay. */
function callAfterTimeout(dispatch: AppDispatch, callback: () => Action) {
	const timeoutId = setTimeout(() => {
		dispatch(callback());
	}, 10000);

	return () => clearTimeout(timeoutId);
}

/** Error handler. Stop sending the form and show error message. */
const handleError = (dispatch: Dispatch, title: string, message: string) => {
	dispatch(costFormActions.resetSending());
	dispatch(
		errorMessageActions.setMessage({
			title,
			message,
		})
	);
	dispatch(errorMessageActions.open());
}

/** Error message when there is no network, user has to resubmit the form 
 * when the network recovers. */
export const noNetworkError = (dispatch: Dispatch) => {
	handleError(
		dispatch,
		'ERROR',
		`It seems you have no network connection. Please try resubmitting 
		your form when your network recovers.`
		)
}

/** Warning message when there is no network, but we'll try sending the form
 * in the backcground. */
export const sendFormLaterError = (dispatch: Dispatch) => {
	handleError(
		dispatch,
		"YOU'RE OFFLINE",
		`It seems you have no network connection. We 
		will attempt to resend your form in the next 48 hours 
		if your network recovers during this time. However, 
		if you don't receive a confirmation email within this period, 
		please try resubmitting your form.`
		)
}

/** Error message when we don't want to provide further details about the error. */
const unKnownError = (dispatch: Dispatch) => {
	handleError(
		dispatch,
		'ERROR',
		`An unknown error occured, apologies for the inconvenience!`,
		)
}

/** Error message when we can't process the image. */
const wrongImageError = (dispatch: Dispatch) => {
	handleError(
		dispatch,
		'ERROR',
		`Unfortunately, we were unable to process the file(s) you've uploaded. 
		Please try another file format!`
	);
}

/** Send expense form to the backend api, display success or error messages,
 * reset form if neccessary. */
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
				callAfterTimeout(dispatch, thankYouMessageActions.close);
				resetForm();

			} else if (response.status === 406) {
				wrongImageError(dispatch);
				resetFileUploader();

			} else {
				unKnownError(dispatch);
			}
		},
		() => {
			if ('serviceWorker' in navigator && 'SyncManager' in window) {
				sendFormLaterError(dispatch)
				resetForm();

			} else {
				noNetworkError(dispatch)
			}
			
		}
	);
	return result;
};
