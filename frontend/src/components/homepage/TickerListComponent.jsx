import * as React from "react";
import { useDispatch, useSelector } from "react-redux";

import tickerServices from '../../data/services/ticker.services';


export default function TickerListComponent(props){
    const dispatch = useDispatch();
    const ticker_manager = useSelector(state => state.tickers);
    const tickers = ticker_manager.main_page_tickers;

    React.useEffect(()=>{
        tickerServices.fetch_main_page_tickers(dispatch);
    }, [])


    const handleSelectedTicker = (id) => {
        props.handleClick(id);
    }

    return (
        <div>
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
                                            <button onClick={()=> handleSelectedTicker(ele.id)} className='btn btn-info'>More...</button>
                                        </div>
                                    </div>
                                    <br />
                                </div>
                            )
                        })}
                    </div>
            </div>
        </div>
    )

}