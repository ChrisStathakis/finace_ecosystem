import * as React from 'react';
import { useDispatch, useSelector } from 'react-redux';

import TickerListComponent from '../components/homepage/TickerListComponent';
import NavbarComponent from '../components/navbar';
import TopNavbarComponent from '../components/TopNavbar';
import tickerServices from '../data/services/ticker.services';
import TickerDetailComponent from '../components/tickers/TickerDetailComponent';

import tickersServices from '../data/services/ticker.services';





export default function  HomepageView() {
    const [showList, setShowList] = React.useState(true);
    const dispatch = useDispatch();
    const navigate = "";
    const ticker_manager = useSelector(state => state.tickers);

    React.useEffect(()=>{
        tickersServices.fetch_main_page_tickers(dispatch);
    }, [])

    const tickers = ticker_manager.main_page_tickers;
    
    const handleSelectTicker = (id) => {
        tickersServices.fetchTicker(id, dispatch);
        setShowList(false);
    }

    return (
        <div>
            <NavbarComponent />
            <main className="main-content border-radius-lg ">
                <TopNavbarComponent />
                {showList ?<TickerListComponent handleClick={handleSelectTicker} /> : <TickerDetailComponent /> }
                
            </main>
        </div>
    )
}