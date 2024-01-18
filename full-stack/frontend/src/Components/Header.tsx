import classes from './Header.module.css';
// import { ReactComponent as Logo } from '../images/logo.svg'
import logoUrl from '../images/thxLogo.png';

function Header() {
    return (
			<header>
				<img
					src={logoUrl}
					width="100"
					height="100"
					className={classes.logo}
					alt="app logo"
				></img>
				<h1 className={classes.header}>Expense Form</h1>
			</header>
		);
}

export default Header;