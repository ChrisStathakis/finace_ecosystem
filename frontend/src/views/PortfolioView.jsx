import * as React from "react";
import { useDispatch, useSelector } from "react-redux";

import NavbarComponent from "../components/navbar";
import TopNavbarComponent from "../components/TopNavbar";
import portfolioServices from "../data/services/portfolioServices"
import tickerServices from "../data/services/ticker.services";
import CreateTickerComponent from "../components/tickers/CreateTickerComponent";
import PortfolioAddTickerComponent from "../components/portfolios/PortfolioAddTickerComponent";


export default function PortfolioView(){
    const [selectTickerId, setSelectTickerID] = React.useState(0);
    const [createTicker, setCreateTicker] = React.useState(false)
    const [addTickerForm, setAddTickerForm] = React.useState(false);
    const [searchName, setSearchName ] = React.useState("");

    const dispatch = useDispatch();

    const portfolio_manager = useSelector(state => state.portfolio);
    const ticker_manager = useSelector(state => state.tickers);
    const profile_manager = useSelector(state => state.profile)
    const portfolio_id = profile_manager.portfolio_id;

    const portfolio = portfolio_manager.port_detail;
    const items = portfolio_manager.port_tickers;
    const tickers = ticker_manager.tickers;
    const ticker = ticker_manager.selectedTicker;


    React.useEffect(()=>{
        console.log("port", portfolio_id, typeof portfolio_id)
        console.log(profile_manager)
        if (portfolio_id !== "undefined"){
            portfolioServices.fetch_portfolio(portfolio_id, dispatch);
            portfolioServices.fetch_user_active_tickers(portfolio_id, dispatch);
        }
        
    }, [portfolio_id])

    React.useEffect(()=>{
        tickerServices.fetchTickers(searchName, dispatch);
    }, [searchName])


    const selectTicker = (id) => {
        setAddTickerForm(true);
        setSelectTickerID(id);

    };

    const handleSell = (ticker) => {
        const data = {
            ...ticker,
            is_sell: true
        };
        portfolioServices.edit_user_ticker(data, portfolio_id, dispatch);
        
    };

    const handleDelete = (id) => {
        portfolioServices.delete_user_ticker(id, portfolio_id, dispatch);
        
    };
    

    return (
        <div>
            <NavbarComponent search_type="tickers" />
            <main className="main-content border-radius-lg ">
                <TopNavbarComponent search_type="tickers" />
                <div className="container-fluid py-4">
                    <div className="row">
                        <div className="col-12">
                            <div className="card">
                                <div className="card-header">
                                    <h4>Items</h4>
                                    <button onClick={()=> setCreateTicker(true)} className="btn btn-info">Create Ticker</button>
                                    {createTicker ? <CreateTickerComponent closeWindow={()=> setCreateTicker(false)} /> : null}
                                </div>
                                <div className="card-body">
                                    <table className="table table-bordered">
                                        <thead>
                                            <tr>
                                                <th>--</th>
                                                <th>CODE | TITLE</th>
                                                <th>STARTING INVESTMENT | QTY</th>
                                                <th>STARTING VALUE | CURRENT VALUE</th>
                                                <th>+/- | +/- % </th>
                                                <th>-</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {items.map((ele)=>{
                                                return (
                                                    <tr>
                                                        <td><button onClick={() => handleDelete(ele.id)} className="btn btn-danger">DELETE</button></td>
                                                        <td>{ ele.code } | {ele.title}</td>
                                                        <td>{ ele.starting_investment } | { ele.qty } %</td>
                                                        <td>
                                                            <span style={{'color': 'red'}}>{ ele.starting_value_of_ticker } € </span> |  
                                                            <span style={{'color': 'green'}}> { ele.current_value_of_ticker } € </span>
                                                        </td>
                                                        <td>
                                                            
                                                            { ele.winning_loosing_situation 
                                                            ? <span style={{'color': 'green'}}> { ele.difference } € | { ele.diff_percent } % </span>
                                                            : <span style={{'color': 'red'}}> { ele.difference } € | { ele.diff_percent } % </span> 
                                                            } 
                                                        </td>
                                                        <td>
                                                            <button onClick={() => handleSell(ele)} className="btn btn-success">SELL</button>
                                                           
                                                        </td>
                                                    </tr>
                                                )
                                            })}
                                        </tbody>
                                        
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    <br /> <br />
                    <div className="row">

                        <div className="col-4">
                            <div className="card">
                                <div className="card-header">
                                    <h4>{portfolio.title}</h4>
                                </div>
                                <div className="card-body">
                                    <ul class="list-group">
                                        <li class="list-group-item">Current Value: {portfolio.current_value} €</li>
                                        <li class="list-group-item">Starting Investment: {portfolio.starting_investment} €</li>
                                        <li class="list-group-item">+/- %: {portfolio.diff_percent} % | +/-: {portfolio.difference} €</li>
                                        <li class="list-group-item">Annual Returns %: {portfolio.annual_returns} %</li>
                                        
                                    </ul>
                                </div>
                            </div>

                            <hr />
                            <div className="card">
                                <div className="card-header">
                                    <h4>Analysis</h4>
                                </div>
                                <div className="card-body">
                                    
                                </div>
                            </div>
                        </div>

                        <div className="col-8">
                            {addTickerForm ? <PortfolioAddTickerComponent ticker={selectTickerId} port={portfolio.id} handleClose={() => setAddTickerForm(false)} />
                            
                        : 
                        
                            <div className="card">
                                <div className="card-header">
                                    <input onChange={(e)=> setSearchName(e.target.value)} value={searchName} className="form-control" placeholder="Search....." />
                                </div>
                                <table className="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th>TICKER</th>
                                            <th>CODE</th>
                                            <th>PRICE</th>
                                            <th>ANNUAL RETURN</th>
                                            <th>+/-</th>
                                            <th>Add</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {tickers.results.map((ele)=>{
                                            return (
                                                <tr>
                                                    <td>{ele.title}</td>
                                                    <td>{ele.ticker}</td>
                                                    <td>{ele.price}</td>
                                                    <td>{ele.annual_returns}</td>
                                                    <td>
                                                        <button onClick={() => selectTicker(ele)} className="btn btn-success">ADD</button>
                                                    </td>
                                                </tr>
                                            )
                                        })}
                                    </tbody>
                                </table>
                            </div>
                            }
                           
                            
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )
}