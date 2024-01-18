/* Loader styling from https://loading.io/css/ */

import classes from './Loader.module.css';
import Modal from './Modal';

const Loader = () => {
	return (
		<Modal>
			<div className={classes.content}>
				<div className={classes.loader}>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
					<div></div>
				</div>
			</div>
		</Modal>
	);
};

export default Loader;
