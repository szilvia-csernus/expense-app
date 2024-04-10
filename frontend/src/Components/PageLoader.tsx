/* Loader styling from https://loading.io/css/ */

import Loader from './Loader';
import Modal from './Modal';

const PageLoader = () => {
	return (
		<Modal>
			<Loader />
		</Modal>
	);
};

export default PageLoader;
