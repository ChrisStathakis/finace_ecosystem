import * as React from "react";
import { useDispatch, useSelector } from "react-redux";

import NavbarComponent from "../components/navbar";
import TopNavbarComponent from "../components/TopNavbar";
import portfolioServices from "../data/services/portfolioServices"
import tickerServices from "../data/services/ticker.services";
import { current } from "@reduxjs/toolkit";
import CreateTickerComponent from "../components/tickers/CreateTickerComponent";
import AddTickerToPortfolioComponent from "../components/portfolios/AddTickerToPortfolio";


export default function PortfolioView(){
    const [selectTickerId, setSelectTickerID] = React.useState(0);
    const [createTicker, setCreateTicker] = React.useState(false)
    const [addTickerForm, setAddTickerForm] = React.useState(false);
    const [showEditTicker, setShowEditTicker] = React.useState(false);
    const [searchName, setSearchName ] = React.useState("");
    const [qty, setQty] = React.useState(0);

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
    }

    const sellTicker = (data) => {
        const new_data = {...data, is_sell: true};
        console.log("Data", new_data)
        portfolioServices.edit_user_ticker(new_data, dispatch);
    }

    const addTickerToPortfolio = (e) => {
        e.preventDefault();
        const data = {
            starting_investment: qty,
            ticker: Number(ticker.id),
            portfolio: portfolio_id,
            qty: 0,
            starting_value_of_ticker: ticker.price,
            current_value: ticker.price,
            is_sell: false,
            price: 0
        }
        console.log("Data to add", data);
        portfolioServices.create_user_ticker(data, dispatch);
    };

    const handleDelete = (id) => {
        portfolioServices.delete_user_ticker(id, portfolio_id, dispatch);
    }
    

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
                                                <th>TICKER</th>
                                                <th>CODE</th>
                                                <th>STARTING VALUE</th>
                                                <th>QTY</th>
                                                <th>CURRENT VALUE</th>
                                                <th>+/-</th>
                                                <th>+/- %</th>
                                                <th>-</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {items.map((ele)=>{
                                                return (
                                                    <tr>
                                                        <td><button onClick={() => handleDelete(ele.id)} className="btn btn-danger">DELETE</button></td>
                                                        <td>{ ele.title }</td>
                                                        <td>{ ele.code }</td>
                                                        <td>{ ele.starting_investment }</td>
                                                        <td>{ ele.qty }</td>
                                                        <td>{ ele.current_value }</td>
                                                        <td>{ ele.ticker }</td>
                                                        <td>{ ele.ticker }</td>
                                                        <td>
                                                            <button onClick={() => sellTicker(ele)} className="btn btn-success">Close </button>
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
                                        <li class="list-group-item">Current Value: {portfolio.current_value}</li>
                                        <li class="list-group-item">Starting Investment: {portfolio.starting_investment}</li>
                                        <li class="list-group-item">Sells: {portfolio.withdraw_value}</li>
                                        <li class="list-group-item">Diff: {portfolio.difference}</li>
                                        <li class="list-group-item">Diff %: {portfolio.diff_percent}</li>
                                        <li class="list-group-item">Annual Returns: {portfolio.annual_returns}</li>
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
                            {addTickerForm ? <AddTickerToPortfolioComponent ticker={selectTickerId} />
                            
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
                                                    <td><button onClick={() => selectTicker(ele.id)} className="btn btn-success">Add</button></td>
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