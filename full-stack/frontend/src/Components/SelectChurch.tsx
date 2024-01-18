import classes from './Form.module.css';
import { SecondaryButton } from './Buttons';
import { useAppDispatch } from '../store/index';
import Modal from './Modal';
import { selectChurchActions } from '../store/select-church-slice';

const SelectChurch = () => {
	const dispatch = useAppDispatch();
	const clickHandler = (event: React.MouseEvent<HTMLButtonElement>) => {
		const target = event.target as HTMLElement;
		dispatch(selectChurchActions.setChurch(target.innerText));
		dispatch(selectChurchActions.close());
	};
	return (
		<Modal>
			<div className={classes.messageContent}>
				<h2>Select Your Church</h2>
				<div>
					<SecondaryButton onClick={clickHandler}>Delft</SecondaryButton>
				</div>
				<br />
				<div>
					<SecondaryButton onClick={clickHandler}>Rotterdam</SecondaryButton>
				</div>
				<br />
			</div>
		</Modal>
	);
};

export default SelectChurch;
