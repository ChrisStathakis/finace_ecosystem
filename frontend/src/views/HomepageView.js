import * as React from 'react';
import NavbarComponent from '../components/navbar';
import TopNavbarComponent from '../components/TopNavbar';
import tickerServices from '../data/services/ticker.services';

import { useDispatch, useSelector } from 'react-redux';




export default function  HomepageView() {
    const dispatch = useDispatch();
    const ticker_manager = useSelector(state => state.tickers);

    React.useEffect(()=>{
        tickerServices.fetch_main_page_tickers(dispatch);
    }, [])

    const tickers = ticker_manager.main_page_tickers;
    

    return (
        <div>
            <NavbarComponent />
            <main className="main-content border-radius-lg ">
                <TopNavbarComponent />
                <div className="container-fluid py-4">
                    <div className='row'>
                        <div className='col-12'><h4>Tickers with the bigger simply return</h4></div>
                    </div>
                    <br />
                    <div className='row'>
                        {tickers.map((ele)=>{
                            return (
                                <div className='col-3'>
                                    <div className='card'>
                                        <div className='card-header'>
                                            <h5>{ele.title}</h5>
                                        </div>
                                        <div className='card-body'>
                                            <ul className="list-group list-group-flush">
                                                <li className="list-group-item">Code:: {ele.ticker}</li>
                                                <li className="list-group-item">Simply Return: {ele.simply_return}</li>
                                                <li className="list-group-item">Market variance: {ele.market_variance}</li>
                                                <li className="list-group-item">Log Return: {ele.log_return}</li>
                                                <li className="list-group-item">Standard Deviation: {ele.standard_deviation}</li>
                                                <li className="list-group-item">Price: {ele.price}</li>
                                        
                                            </ul>
                                            <button className='btn btn-info'>More...</button>
                                        </div>
                                    </div>
                                    <br />
                                </div>
                            )
                        })}
                    </div>
                </div>
            </main>
        </div>
    )
}