import { configureStore } from '@reduxjs/toolkit';
import costFormSlice from './cost-form-slice';
import thankYouMessageSlice from './thank-you-message-slice';
import errorMessageSlice from './error-message-slice';
import churchSlice from './church-slice';

import { useDispatch, useSelector, type TypedUseSelectorHook } from 'react-redux';


const store = configureStore({
	reducer: {
		church: churchSlice.reducer,
		costForm: costFormSlice.reducer,
		thankYouMessage: thankYouMessageSlice.reducer,
		errorMessage: errorMessageSlice.reducer,
	}
});

export type RootState = ReturnType<typeof store.getState>;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

export type AppDispatch = typeof store.dispatch;
export const useAppDispatch: () => AppDispatch = useDispatch;

export default store;
