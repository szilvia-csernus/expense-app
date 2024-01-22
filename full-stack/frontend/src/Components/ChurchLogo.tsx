import classes from './Form.module.css';

import { useAppSelector } from '../store';

const ChurchLogo = () => {
	const churchValue = useAppSelector(state => state.church.church);
	const churchLogo = useAppSelector(state => state.church.logo);
	const logo = (
		<img
			src={churchLogo}
			width="270"
			height="80"
			className={classes.churchLogo}
			alt="church logo"
		></img>
	);
	return <>{churchValue && logo}</>;
};

export default ChurchLogo;
