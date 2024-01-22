import Header from '../Components/Header';
import CostForm from '../Components/CostForm';
import Footer from '../Components/Footer';
import { Container } from '../Components/Container';
import ThankYouMessage from '../Components/ThankYouMessage';
import ErrorMessage from '../Components/ErrorMessage';
import Loader from '../Components/Loader';
import SelectChurch from '../Components/SelectChurch';

import { useAppDispatch, useAppSelector } from '../store';
import { useEffect } from 'react';
import { getChurchDetails, getChurches } from '../store/church-action-creators';

function Home() {
    const selectChurchStatus = useAppSelector(state => state.church.status)
    const thankYouMessage = useAppSelector(state => state.thankYouMessage);
    const errorMessage = useAppSelector(state => state.errorMessage.status);
    const sending = useAppSelector(state => state.costForm.sending);
    const church = useAppSelector(state => state.church.church);
    const dispatch = useAppDispatch();

    useEffect(() => {
        church && getChurchDetails(dispatch, church);
        getChurches(dispatch)
    }, [dispatch, church]);

    return (
        <Container>
            <Header />
            {selectChurchStatus && <SelectChurch />}
            {sending && <Loader />}
            {thankYouMessage && <ThankYouMessage/>}
            {errorMessage && <ErrorMessage/>}
            <CostForm />
            <Footer />
        </Container>
    )
}

export default Home;