import * as React from "react";
import { useDispatch, useSelector } from "react-redux";

import NavbarComponent from "../components/navbar";
import TopNavbarComponent from "../components/TopNavbar";
import portfolioServices from "../data/services/portfolioServices"
import tickerServices from "../data/services/ticker.services";


export default function PortfolioDetailView(){
    const [addTickerForm, setAddTickerForm] = React.useState(false);
    const [showEditTicker, setShowEditTicker] = React.useState(false);
    
    const [qty, setQty] = React.useState(0);

    const dispatch = useDispatch();

    const portfolio_manager = useSelector(state => state.portfolio);
    const ticker_manager = useSelector(state => state.tickers);
    const portfolio_id = portfolio_manager.portfolio_id;

    const portofolio = portfolio_manager.port_detail;
    const items = portfolio_manager.port_tickers;
    const tickers = ticker_manager.tickers;
    const ticker = ticker_manager.selectedTicker;

    React.useEffect(()=>{
        if (portfolio_id !== null){
            portfolioServices.fetch_portfolio(portfolio_id, dispatch);
            portfolioServices.fetch_user_tickers(portfolio_id, dispatch);
        }
        
    }, [portfolio_id])

    const selectTicker = (id) => {
        console.log("id", id)
        setAddTickerForm(true);
        tickerServices.fetchTicker(id, dispatch);
    }

    const addTickerToPortfolio = (e) => {
        e.preventDefault();
        const data = {
            starting_investment: qty,
            ticker: ticker.id,
            portfolio: portfolio_id,
            qty: 0,
            starting_value_of_ticker: ticker.price
        }
        console.log("data", data)
        portfolioServices.create_user_ticker(data, dispatch)
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
                                </div>
                                <div className="card-body">
                                    <table className="table table-bordered">
                                        <thead>
                                            <tr>
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
                                                        <td>{ ele.title }</td>
                                                        <td>{ ele.code }</td>
                                                        <td>{ ele.starting_investment }</td>
                                                        <td>{ ele.qty }</td>
                                                        <td>{ ele.current_value }</td>
                                                        <td>{ ele.ticker }</td>
                                                        <td>{ ele.ticker }</td>
                                                        <td>
                                                            <button className="btn btn-info">Edit</button>
                                                            <button className="btn btn-danger">Close </button>
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
                                    <h4>{portofolio.title}</h4>
                                </div>
                                <div className="card-body">
                                    <ul class="list-group">
                                        <li class="list-group-item">Current Value: {portofolio.current_value}</li>
                                        <li class="list-group-item">Starting Investment: {portofolio.starting_investment}</li>
                                        <li class="list-group-item">A third item</li>
                                        <li class="list-group-item">Variance: {portofolio.variance}</li>
                                        <li class="list-group-item">Annual Returns: {portofolio.annual_returns}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div className="col-8">
                            {addTickerForm ?
                            <div className="card">
                                <div className="card-header">
                                    <h4>{ticker.title}</h4>
                                    <button onClick={() => setAddTickerForm(false)} className="btn btn-warning">Close</button>
                                </div>
                                <div className="card-body"> 
                                    <form className="form">
                                        <div className="form-group">
                                            <label>Add the Invest</label>
                                            <input value={qty} onChange={(e)=> setQty(e.target.value)} style={{borderBlockColor: "grey"}} type="number" step="0.001" className="form-control"  />
                                        </div>
                                        <button onClick={(e)=> addTickerToPortfolio(e)}  className="btn btn-success">Add to Portfolio</button>
                                    </form>
                                </div>
                            </div>
                        : 
                        
                            <div className="card">
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