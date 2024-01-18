import Header from '../Components/Header';
import CostForm from '../Components/CostForm';
import Footer from '../Components/Footer';
import { Container } from '../Components/Container';
import ThankYouMessage from '../Components/ThankYouMessage';
import ErrorMessage from '../Components/ErrorMessage';
import Loader from '../Components/Loader';
import SelectChurch from '../Components/SelectChurch';

import { useAppSelector } from '../store';

function Home() {
    const selectChurch = useAppSelector(state => state.selectChurch.status)
    const thankYouMessage = useAppSelector(state => state.thankYouMessage);
    const errorMessage = useAppSelector(state => state.errorMessage.status);
    const sending = useAppSelector(state => state.costForm.sending);

    return (
        <Container>
            <Header />
            {selectChurch && <SelectChurch />}
            {sending && <Loader />}
            {thankYouMessage && <ThankYouMessage/>}
            {errorMessage && <ErrorMessage/>}
            <CostForm />
            <Footer />
        </Container>
    )
}

export default Home;