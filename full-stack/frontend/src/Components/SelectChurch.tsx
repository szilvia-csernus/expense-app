import classes from './Form.module.css';
import { SecondaryButton } from './Buttons';
import { useAppDispatch, useAppSelector } from '../store/index';
import Modal from './Modal';
import { churchActions } from '../store/church-slice';

const SelectChurch = () => {
	const churches = useAppSelector((state) => state.church.churches);
	const dispatch = useAppDispatch();

	const clickHandler = (event: React.MouseEvent<HTMLButtonElement>) => {
		const target = event.target as HTMLElement;
		dispatch(churchActions.setChurch(target.innerText));
		dispatch(churchActions.close());
	};
	return (
		<Modal>
			<div className={classes.messageContent}>
				<h2>Select Your Church</h2>
				{churches.map((church) => (
					<div key={church}>
						<div>
							<SecondaryButton onClick={clickHandler}>{church}</SecondaryButton>
						</div>
						<br />
					</div>
				))}
			</div>
		</Modal>
	);
};

export default SelectChurch;
