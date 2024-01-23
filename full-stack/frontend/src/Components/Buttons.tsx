import classes from './Buttons.module.css';

interface ButtonProps {
	onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
	children: React.ReactNode;
}

type GeneralButtonProps = ButtonProps & {
	type: 'button' | 'submit' | 'reset';
	className: string;
};

export const GeneralButton = (props: GeneralButtonProps) => {
	const classNames = `${classes.button} ${props.className}`;
	return (
		<button type={props.type} className={classNames} onClick={props.onClick}>
			{props.children}
		</button>
	);
};

export const SecondaryButton = (props: ButtonProps) => {
	return (
		<GeneralButton
			type="button"
			className={classes.secondaryButton}
			onClick={props.onClick}
		>
			{props.children}
		</GeneralButton>
	);
};

export const SubmitButton = (props: ButtonProps) => {
	return (
		<GeneralButton
			type="submit"
			className={classes.primaryButton}
		>
			{props.children}
		</GeneralButton>
	);
};

export const DeleteButton = (props: ButtonProps) => {
	return (
		<GeneralButton
			type="button"
			className={classes.deleteButton}
			onClick={props.onClick}
		>
			{props.children}
		</GeneralButton>
	);
};

export const PrimaryButton = (props: ButtonProps) => {
	return (
		<GeneralButton
			type="button"
			className={classes.primaryButton}
			onClick={props.onClick}
		>
			{props.children}
		</GeneralButton>
	);
};