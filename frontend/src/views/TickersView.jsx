import * as React from "react";
import { useDispatch, useSelector } from 'react-redux';

import NavbarComponent from "../components/navbar";
import TopNavbarComponent from "../components/TopNavbar";
import tickersService from "../data/services/ticker.services";
import TickerListComponent from "../components/tickers/TickerListComponent";
import TickerDetailComponent from "../components/tickers/TickerDetailComponent";



export default function TickersView(){
    const [showList, setShowList] = React.useState(true);
    const dispatch = useDispatch();

    const handleSelectedTicker = (id) => {
        tickersService.fetchTicker(id, dispatch);
        setShowList(false);
    }

    return (
        <div>
            <NavbarComponent search_type="tickers" />
            <main className="main-content border-radius-lg ">
                <TopNavbarComponent search_type="tickers" />
                {showList ?  <TickerListComponent handleClick={handleSelectedTicker} /> : <TickerDetailComponent closeWindow={setShowList(true)} />}
            </main>

        </div>
        
    )
};



