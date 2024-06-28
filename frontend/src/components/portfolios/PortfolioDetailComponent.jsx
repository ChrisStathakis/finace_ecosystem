import * as React from "react";
import {useDispatch, useSelector} from "react-redux";

import tickerServices from "../../data/services/ticker.services";
import portfolioService from "../../data/services/portfolioServices";
import NavbarComponent from "../navbar";
import TopNavbarComponent from "../TopNavbar";
import AddTickerToPortfolio from "./AddTickerToPortfolio";


export default function PortfolioDetailComponent(){
    const [showAddTicker, setShowAddTicker] = React.useState(false);
    const [selectedTicker, setSelectedTicker] = React.useState(0);
    const [q, setQ] = React.useState("");

    const dispatch = useDispatch();

    const port_manager = useSelector(state=>state.portfolio);
    const ticker_manager = useSelector(state => state.tickers);

    const tickers = ticker_manager.tickers.results;
    const portfolio = port_manager.port_detail;
    const port_tickers = port_manager.port_tickers

    React.useEffect(()=>{
        tickerServices.fetchTickers("", dispatch);
    }, []);
    
    React.useEffect(()=>{
        
        if (portfolio.id !== undefined){
            portfolioService.fetch_user_tickers(portfolio.id, dispatch)
        }
       
    }, [portfolio]);

    const closeCreateWindow = () => {setShowAddTicker(false)}
    const selectAddTicker = (id) => {setSelectedTicker(id); setShowAddTicker(true);};
    const handleSearh = (e) => {
        e.preventDefault();
        setQ(e.target.value);
        if (e.length > 1){
            tickerServices.fetchTickers(q, dispatch);
        }
    }

    return (
        <div>
            <NavbarComponent />
            <main className="main-content border-radius-lg">
                <TopNavbarComponent />
                <div className="container-fluid py-4">
                    <div className="row">
                        <div className="col-4">
                            <div className="card">
                                <div className="card-header">
                                    <h4>{portfolio.title}</h4>
                                </div>
                                <div className="card-body">
                                    <ul className="list-group list-group-flush">
                                        <li className="list-group-item">Starting investment: {portfolio.starting_investment}</li>
                                        <li className="list-group-item">Current Value: {portfolio.currunt_value}</li>
                                        <li className="list-group-item">Annual Returns: {portfolio.annual_returns}</li>
                                        <li className="list-group-item">Variance: {portfolio.variance}</li>
                                       
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div className="col-8">
                            <table className="table table-bordered">
                                <thead>
                                    <tr>
                                        <th>Title</th>
                                        <th>Code</th>
                                        <th>Qty</th>
                                        <th>Starting Price</th>
                                        <th>Current Price</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {port_tickers.map((ele)=>{return(
                                        <tr>

                                        </tr>
                                    )})}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <hr />
                    <br />
                    <hr />
                    <div className="row">
                        <div className="col-4">
                            {showAddTicker ? <AddTickerToPortfolio closeWindow={closeCreateWindow} ticker={selectedTicker} /> :
                            <div className="card">
                                <div className="card-header">
                                   <h5>Add Ticker</h5>
                                   <input onChange={(e)=> handleSearh(e)} type="text" className="form-control" placeholder="Search" style={{backgroundColor: '#f0f8ff'}}/>
                                </div>
                                <div className="card-body">
                                    <table className="table">
                                        <thead>
                                            <tr>
                                                <th>Ticker</th>
                                                <th>Code</th>
                                                <th>-</th>
                                                <th>-</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {tickers.map((ele)=>{
                                                return (
                                                    <tr>
                                                        <td>{ele.title}</td>
                                                        <td>{ele.ticker}</td>
                                                        <td><button onClick={() => selectAddTicker(ele.id)} className="btn btn-success">Add</button></td>
                                                        <td><button onClick={() => selectAddTicker(ele.id)} className="btn btn-primary">Detail</button></td>
                                                    </tr>
                                                )
                                            })}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            }
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )

}