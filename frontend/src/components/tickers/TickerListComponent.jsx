import * as React from "react";
import { useDispatch, useSelector } from 'react-redux';
import tickersService from "../../data/services/ticker.services";
import CreateTickerComponent from "./CreateTickerComponent";



export default function TickerListComponent(props){
    const [showCreateView, setShowCreateView] = React.useState(false);
    const tickerManager = useSelector(state => state.tickers);
    const dispatch = useDispatch();

    const tickers = tickerManager.tickers;
    const [q, setQ] = React.useState("");

    React.useEffect(()=>{
        tickersService.fetchTickers("", dispatch);
    }, [])

    const handleClick = (id) => {
        props.handleClick(id);
    }

    return (
        <div className="container-fluid py-4">
                    <div className="row">
                        <div className="col-12">
                            <div className="card">
                                <div className="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
                                    <div className="bg-gradient-primary shadow-primary border-radius-lg pt-4 pb-3">
                                        <h6 className="text-white text-capitalize ps-3">Tickers</h6>
                                        
                                    </div>
                                </div>
                                <div className="card-body px-0 pb-2">
                                    <button onClick={() => setShowCreateView(true)} className="btn btn-primary">CREATE TICKER</button>
                                    {showCreateView ? <CreateTickerComponent closeWindow={()=> setShowCreateView(false)} /> : null}
                                    <div className="table-responsive p-0">
                                        <table className="table align-items-center mb-0">
                                        <thead>
                                            <tr>
                                                <th className="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">ID</th>
                                                <th className="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Ticker</th>
                                                <th className="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Code</th>
                                                <th className="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Beta</th>
                                                <th className="text-secondary opacity-7">Return</th>
                                                <th>-</th>
                                                </tr>
                                        </thead>
                                        <tbody>
                                            {
                                                
                                                    tickers.results.map((ticker)=>{
                                                        return (
                                                            <tr>
                                                                <td>{ticker.id}</td>
                                                                <td>{ticker.title}</td>
                                                                <td>{ticker.ticker}</td>
                                                                <td>{ticker.beta}</td>
                                                                <td>{ticker.simply_return}</td>
                                                                <td><button onClick={()=> handleClick(ticker.id)} className="btn btn-info">Details</button></td>
                                                            </tr>
                                                        )
                                                    })
                                                   
                                            }
                                        
                                        </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
          
        
    )
};



