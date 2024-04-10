import classes from './Container.module.css';

interface ContainerProps {
	className?: string;
	children: React.ReactNode;
}

export const Container = (props: ContainerProps) => {
	const classNames = `${classes.container} ${props.className ? props.className : ""}`;
	return <div className={classNames}>{props.children}</div>;
};
