import classes from './Form.module.css';
import { DeleteButton } from './Buttons';
import { useAppSelector } from '../store/index';
import { Dispatch, SetStateAction, useEffect, useId } from 'react';

type FileUploaderType = {
	selectedFile: File | null;
	setSelectedFile: Dispatch<SetStateAction<File | null>>;
	fileError: string | boolean;
	setFileError: Dispatch<SetStateAction<string | boolean>>;
	fileList: File[] | [];
	setFileList: Dispatch<SetStateAction<File[] | []>>;
	totalFileSize: number;
	setTotalFileSize: Dispatch<SetStateAction<number>>;
};

const FileUploader = ({
	setSelectedFile,
	fileError,
	setFileError,
	fileList,
	setFileList,
	totalFileSize,
	setTotalFileSize,
}: FileUploaderType) => {
	const submitting = useAppSelector((state) => state.costForm.submitting);
	const id = useId();
	const receiptsClassNames = `${classes.formInput} 
                                ${fileError && classes.fileInputInvalid} 
                                ${classes.customFileUploadButton}`;

	const addFileToList = (file: File) => {
		setFileList((prevList) => [...prevList, file]);
		setTotalFileSize((prevSize) => prevSize + file.size);
	};

	const removeFileFromList = (file: File) => {
		setFileList((prevList) => prevList.filter((f) => f !== file));
		setTotalFileSize((prevSize) => prevSize - file.size);
	};

	useEffect(() => {
		if (submitting) {
			if (fileList.length === 0) {
				setFileError('Please upload a picture of the receipt.');
			}
		}
	}, [submitting, fileList, setFileError, totalFileSize]);

	const fileUploadIsValid = (file: File) => {
		const fileTypes = [
			'image/png',
			'image/jpeg',
			'image/jpg',
			'application/pdf',
		];
		const fileSize = file.size;
		const fileType = file.type;
		if (!fileTypes.includes(fileType)) {
			setFileError('File type not supported');
			setTimeout(() => setFileError(false), 3000);
			return false;
		} else if (totalFileSize + fileSize > 5.5 * 1024 * 1024) {
			setFileError('Total file size cannot exceed 5 MB');
			setTimeout(() => setFileError(false), 5000);
			return false;
		}
		setFileError(false);
		return true;
	};

	const handleFileInput = (event: React.ChangeEvent<HTMLInputElement>) => {
		if (event.target.files && event.target.files.length > 0) {
			const file = event.target.files[0];
			if (fileUploadIsValid(file)) {
				setSelectedFile(file);
				addFileToList(file);
			}
		}
	};

	const handleOnClick = () => {
		setFileError(false);
	};

	const showFileList = (
		<ul>
			{fileList.map((file: File) => {
				return (
					<li className={classes.fileListItem} key={id}>
						<DeleteButton onClick={() => removeFileFromList(file)}>
							X
						</DeleteButton>
						{file.name} -{' '}
						{file.size < (1024 * 1024)
							? `${(file.size / 1024).toFixed(0)} kB`
							: `${(file.size / 1024 / 1024).toFixed(2)} MB`}
					</li>
				);
			})}
		</ul>
	);

	return (
		<>
			{showFileList}
			<br />
			<div className={classes.uploadButtonFrame}>
				<label htmlFor="receipts" className={receiptsClassNames}>
					Add Photo
				</label>
			</div>
			<input
				id="receipts"
				type="file"
				name="receipts"
				className={classes.fileInputField}
				accept="image/png, image/jpeg, image/jpg, application/pdf"
				onChange={handleFileInput}
				onClick={handleOnClick}
			/>
			<div
				className={fileError ? classes.feedbackInvalid : classes.feedbackValid}
			>
				{fileError}
			</div>
		</>
	);
};

export default FileUploader;
