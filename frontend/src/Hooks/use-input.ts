import { useState } from "react";

export type ValidateType = (arg: string) => boolean;

const useInput = (validateInput: ValidateType) => {

    const [enteredValue, setEnteredValue] = useState('');
    const [isTouched, setIsTouched] = useState(false);

    const valueIsValid = validateInput(enteredValue);
    const hasError = (valueIsValid === false) && isTouched;

    const inputChangeHandler = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
			setEnteredValue(event.target.value);
		};

    const inputBlurHandler = () => {
       setIsTouched(true);
    }

    const reset = () => {
       setEnteredValue('');
       setIsTouched(false)
    }

    return {
        value: enteredValue,
        isValid: valueIsValid,
        hasError,
        inputChangeHandler,
        inputBlurHandler,
        reset
    }
}

export default useInput;