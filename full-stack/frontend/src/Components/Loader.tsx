/* Loader styling from https://loading.io/css/ */

import classes from './Loader.module.css';

const Loader = () => {
	return (
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
	);
};

export default Loader;
