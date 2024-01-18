import classes from './Buttons.module.css';

export const SubmitButton = (props) => {
	const classNames = `${classes.button} ${classes.primaryButton}`;
	return (
		<button type="submit" className={classNames} onClick={props.onClick}>
			{props.children}
		</button>
	);
};

export const DeleteButton = (props) => {
	const classNames = `${classes.button} ${classes.deleteButton}`;
	return (
		<button type="button" className={classNames} onClick={props.onClick}>
			{props.children}
		</button>
	);
};

export const PrimaryButton = (props) => {
	const classNames = `${classes.button} ${classes.primaryButton}`;
	return (
		<button type="button" className={classNames} onClick={props.onClick}>
			{props.children}
		</button>
	);
}

export const SecondaryButton = (props) => {
	const classNames = `${classes.button} ${classes.secondaryButton}`;
	return (
		<button type="button" className={classNames} onClick={props.onClick}>
			{props.children}
		</button>
	);
}