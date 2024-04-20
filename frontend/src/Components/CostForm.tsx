import classes from './Form.module.css';

import { useState, useEffect } from 'react';
import useInput, { type ValidateType } from '../Hooks/use-input';
import { SubmitButton } from './Buttons';
import FileUploader from './FileUploader';
import { noNetworkError, send } from '../store/form-action-creators';
import { useAppSelector } from '../store/index';
import { costFormActions } from '../store/cost-form-slice';
import { churchActions } from '../store/church-slice';
import ChurchLogo from './ChurchLogo';
import { useAppDispatch } from '../store/index';
import Loader from './Loader';

const isNotEmpty: ValidateType = (value) => value.trim() !== '';
const isEmail: ValidateType = (value) =>
	/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(value);
const noValidate = () => true;

const CostForm = () => {
	const [formValid, setFormValid] = useState(false);
	// file uploads are not allowed to be stored in redux store
	// https://redux-toolkit.js.org/usage/usage-guide#working-with-non-serializable-data
	// however, the solution above did not work for me hence I'm using useState here
	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [fileError, setFileError] = useState<string | boolean>(false);
	const [fileList, setFileList] = useState<File[] | []>([]);
	const [totalFileSize, setTotalFileSize] = useState<number>(0);

	const purposes = useAppSelector((state) => state.church.costPurposes);
	const churchValue = useAppSelector((state) => state.church.church);
	const fetchingInProcess = useAppSelector(
		(state) => state.church.fetchingDetailsInProcess
	);

	const dispatch = useAppDispatch();

	const handleSelectChurch = () => {
		dispatch(churchActions.open());
		purposeReset();
	};

	const {
		value: nameValue,
		isValid: nameIsValid,
		hasError: nameHasError,
		inputChangeHandler: nameChangeHandler,
		inputBlurHandler: nameBlurHandler,
		reset: nameReset,
	} = useInput(isNotEmpty);

	const {
		value: emailValue,
		isValid: emailIsValid,
		hasError: emailHasError,
		inputChangeHandler: emailChangeHandler,
		inputBlurHandler: emailBlurHandler,
		reset: emailReset,
	} = useInput(isEmail);

	const {
		value: dateValue,
		isValid: dateIsValid,
		hasError: dateHasError,
		inputChangeHandler: dateChangeHandler,
		inputBlurHandler: dateBlurHandler,
		reset: dateReset,
	} = useInput(isNotEmpty);

	const {
		value: descriptionValue,
		isValid: descriptionIsValid,
		hasError: descriptionHasError,
		inputChangeHandler: descriptionChangeHandler,
		inputBlurHandler: descriptionBlurHandler,
		reset: descriptionReset,
	} = useInput(isNotEmpty);

	const {
		value: purposeValue,
		isValid: purposeIsValid,
		hasError: purposeHasError,
		inputChangeHandler: purposeChangeHandler,
		inputBlurHandler: purposeBlurHandler,
		reset: purposeReset,
	} = useInput(isNotEmpty);

	const {
		value: totalValue,
		isValid: totalIsValid,
		hasError: totalHasError,
		inputChangeHandler: totalChangeHandler,
		inputBlurHandler: totalBlurHandler,
		reset: totalReset,
	} = useInput(isNotEmpty);

	const {
		value: ibanValue,
		isValid: ibanIsValid,
		hasError: ibanHasError,
		inputChangeHandler: ibanChangeHandler,
		inputBlurHandler: ibanBlurHandler,
		reset: ibanReset,
	} = useInput(noValidate);

	const {
		value: accountNameValue,
		isValid: accountNameIsValid,
		hasError: accountNameHasError,
		inputChangeHandler: accountNameChangeHandler,
		inputBlurHandler: accountNameBlurHandler,
		reset: accountNameReset,
	} = useInput(noValidate);

	useEffect(() => {
		if (
			nameIsValid &&
			emailIsValid &&
			dateIsValid &&
			descriptionIsValid &&
			purposeIsValid &&
			totalIsValid &&
			fileList.length > 0 &&
			!fileError &&
			ibanIsValid &&
			accountNameIsValid
		) {
			setFormValid(true);
		}
		return () => setFormValid(false);
	}, [
		nameIsValid,
		emailIsValid,
		dateIsValid,
		descriptionIsValid,
		purposeIsValid,
		totalIsValid,
		fileList,
		fileError,
		ibanIsValid,
		accountNameIsValid,
	]);

	const submitHandler = (event: React.FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		dispatch(costFormActions.setSubmitting());

		if (!formValid) {
			nameBlurHandler();
			emailBlurHandler();
			dateBlurHandler();
			descriptionBlurHandler();
			purposeBlurHandler();
			totalBlurHandler();
			ibanBlurHandler();
			accountNameBlurHandler();
			return;
		} else {
			const formData = new FormData();

			formData.set('church', churchValue);
			formData.set('name', nameValue);
			formData.set('email', emailValue);
			formData.set('date', dateValue);
			formData.set('description', descriptionValue);
			formData.set('purpose', purposeValue);
			formData.set('total', totalValue);
			for (let i = 0; i < fileList.length; i++) {
				formData.set(`receipt${i}`, fileList[i]);
			}
			formData.set('iban', ibanValue);
			formData.set('accountName', accountNameValue);

			const resetForm = () => {
				nameReset();
				emailReset();
				dateReset();
				descriptionReset();
				purposeReset();
				totalReset();
				setSelectedFile(null);
				setFileList([]);
				setFileError(false);
				setTotalFileSize(0);
				ibanReset();
				accountNameReset();
			};

			const resetFileUploader = () => {
				setSelectedFile(null);
				setFileList([]);
				setFileError(false);
				setTotalFileSize(0);
			};

			// We check if the user is using an IOS device. We need to check this
			// as the backgroundSync is inconsistent on IOS and as such we
			// don't want to send the form if the user is offline.
			// This piece of code can be changed once backgroundSync is fully suppported on
			// these devices.
			const isIOS = /iPad|iPhone/.test(navigator.userAgent);
			if (isIOS && !navigator.onLine) {
				noNetworkError(dispatch)
			} else {
				send(dispatch, formData, resetForm, resetFileUploader);
			}

			dispatch(costFormActions.resetSubmitting());
		}
	};

	const nameClassNames = `${classes.formInput} ${
		nameHasError && classes.formInputInvalid
	}`;
	const emailClassNames = `${classes.formInput} ${
		emailHasError && classes.formInputInvalid
	}`;
	const dateClassNames = `${classes.formInput} ${
		dateHasError && classes.formInputInvalid
	}`;
	const descriptionClassNames = `${classes.formInput} ${
		descriptionHasError && classes.formInputInvalid
	}`;
	const purposeClassNames = `${classes.formInput} ${
		purposeHasError && classes.formInputInvalid
	}`;
	const totalClassNames = `${classes.formInput} ${
		totalHasError && classes.formInputInvalid
	}`;
	const ibanClassNames = `${classes.formInput} ${
		ibanHasError && classes.formInputInvalid
	}`;
	const accountNameClassNames = `${classes.formInput} ${
		accountNameHasError && classes.formInputInvalid
	}`;

	return (
		<section className={classes.content}>
			{fetchingInProcess && <Loader />}

			{!fetchingInProcess && (
				<>
					<ChurchLogo />
					<br />
					<div className={classes.formBody}>
						<form className={classes.form} onSubmit={submitHandler}>
							{/* PERSONAL INFORMATION */}
							<fieldset>
								<h2>Personal Information</h2>

								{/* Name  */}
								<label htmlFor="name" className={classes.labelText}>
									Name *
								</label>
								<p className={classes.labelSubText}>
									Please give your name here in case we need to contact you.
								</p>
								<input
									id="name"
									type="text"
									name="name"
									className={nameClassNames}
									onChange={nameChangeHandler}
									onBlur={nameBlurHandler}
									value={nameValue}
									autoComplete="name"
									maxLength={200}
								/>
								<div
									className={
										nameHasError
											? classes.feedbackInvalid
											: classes.feedbackValid
									}
								>
									Please provide your name.
								</div>

								{/* Email  */}
								<label htmlFor="email" className={classes.labelText}>
									Email address *
								</label>
								<p className={classes.labelSubText}>
									Your email address where we can reach you.
								</p>
								<input
									id="email"
									type="email"
									name="email"
									className={emailClassNames}
									onChange={emailChangeHandler}
									onBlur={emailBlurHandler}
									value={emailValue}
									autoComplete="email"
									maxLength={100}
								/>
								<div
									className={
										emailHasError
											? classes.feedbackInvalid
											: classes.feedbackValid
									}
								>
									Please provide your email address.
								</div>
							</fieldset>

							{/* EXPENSES */}
							<fieldset>
								<h2>Expenses</h2>

								{/* Selected Church  */}
								<p className={classes.labelSubText}>
									Your Selected Church is <strong>{churchValue}</strong>. Is
									this not your church?{' '}
									<span onClick={handleSelectChurch} className={classes.linkText}>
										Change it here.
									</span>
								</p>

								{/* Purpose  */}
								<label htmlFor="purpose" className={classes.labelText}>
									Purpose *
								</label>
								<p className={classes.labelSubText}>
									Please select a purpose for the expense.
								</p>
								<select
									id="purpose"
									name="purpose"
									className={purposeClassNames}
									onChange={purposeChangeHandler}
									onBlur={purposeBlurHandler}
									value={purposeValue}
								>
									<option value="" disabled>
										Select a purpose
									</option>
									{purposes.map((purpose) =>
										purpose.cost_code ? (
											<option
												key={`${purpose.name} ${purpose.cost_code}`}
												value={`${purpose.name} (${purpose.cost_code})`}
											>
												{`${purpose.name} (${purpose.cost_code})`}
											</option>
										) : (
											<option key={purpose.name} value={purpose.name}>
												{purpose.name}
											</option>
										)
									)}
								</select>

								<div
									className={
										purposeHasError
											? classes.feedbackInvalid
											: classes.feedbackValid
									}
								>
									Please select a purpose.
								</div>

								{/* Date  */}
								<label htmlFor="date" className={classes.labelText}>
									Date of expense (on receipt) *
								</label>
								<p className={classes.labelSubText}>
									If you have many receipts, then use the date from the latest.
									If they relate to multiple years, then it is best to group
									them by years into separate submissions to help our
									bookkeeping.
								</p>
								<input
									id="date"
									type="date"
									name="date"
									className={dateClassNames}
									onChange={dateChangeHandler}
									onBlur={dateBlurHandler}
									value={dateValue}
								/>
								<div
									className={
										dateHasError
											? classes.feedbackInvalid
											: classes.feedbackValid
									}
								>
									Please select a date.
								</div>

								{/* Description  */}
								<label htmlFor="description" className={classes.labelText}>
									Description *
								</label>
								<p className={classes.labelSubText}>
									Short description for the expense.
								</p>
								<input
									id="description"
									type="text"
									name="description"
									className={descriptionClassNames}
									onChange={descriptionChangeHandler}
									onBlur={descriptionBlurHandler}
									value={descriptionValue}
									maxLength={200}
								/>
								<div
									className={
										descriptionHasError
											? classes.feedbackInvalid
											: classes.feedbackValid
									}
								>
									Please provide a short description.
								</div>

								{/* Total  */}
								<label htmlFor="total" className={classes.labelText}>
									Total *
								</label>
								<p className={classes.labelSubText}>
									The total amount in EUR to be reimbursed.
								</p>
								<input
									id="total"
									type="total"
									name="total"
									className={totalClassNames}
									onChange={totalChangeHandler}
									onBlur={totalBlurHandler}
									value={totalValue}
									maxLength={10}
								/>
								<div
									className={
										totalHasError
											? classes.feedbackInvalid
											: classes.feedbackValid
									}
								>
									Invalid amount.
								</div>

								{/* Receipts  */}
								<span className={classes.labelText}>Receipt(s) *</span>
								<p className={classes.labelSubText}>
									Please take/upload a clear picture or PDF of the receipt of
									the expense made. Accepted file types: png, jpg, jpeg, pdf.
									Max upload: 5MB.
								</p>

								<FileUploader
									selectedFile={selectedFile}
									setSelectedFile={setSelectedFile}
									fileError={fileError}
									setFileError={setFileError}
									fileList={fileList}
									setFileList={setFileList}
									totalFileSize={totalFileSize}
									setTotalFileSize={setTotalFileSize}
								/>
							</fieldset>

							{/* REIMBURSEMENT DETAILS  */}
							<fieldset>
								<h2>Reimbursement Details (optional)</h2>
								{/* Bank Account  */}
								<label htmlFor="iban" className={classes.labelText}>
									Bank Account Number (IBAN)
								</label>
								<p className={classes.labelSubText}>
									If you are not a regular donor of our church, then please give
									us an IBAN where we can send you the reimbursement.
								</p>
								<input
									id="iban"
									type="text"
									name="iban"
									className={ibanClassNames}
									onChange={ibanChangeHandler}
									onBlur={ibanBlurHandler}
									value={ibanValue}
									autoComplete="on"
									maxLength={34}
								/>
								<div
									className={
										ibanHasError
											? classes.feedbackInvalid
											: classes.feedbackValid
									}
								>
									Please provide your bank account number.
								</div>

								{/* Name of Bank Account Holder  */}
								<label htmlFor="accountName" className={classes.labelText}>
									Name of Bank Account Holder
								</label>
								<p className={classes.labelSubText}>
									Please enter the name of the account holder if it is different
									from the name entered at the top of this form.
								</p>
								<input
									id="accountName"
									type="accountName"
									name="accountName"
									className={accountNameClassNames}
									onChange={accountNameChangeHandler}
									onBlur={accountNameBlurHandler}
									value={accountNameValue}
									maxLength={200}
								/>
								<div
									className={
										accountNameHasError
											? classes.feedbackInvalid
											: classes.feedbackValid
									}
								>
									Invalid name.
								</div>
							</fieldset>

							<br />
							<div className={classes.footer}>
								<SubmitButton>Submit</SubmitButton>
							</div>
						</form>
					</div>
				</>
			)}
		</section>
	);
};

export default CostForm;
