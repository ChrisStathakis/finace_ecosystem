import * as React from "react";
import { useDispatch, useSelector } from "react-redux";

import portfolioServices from "../../data/services/portfolioServices";


export default function AddTickerToPortfolioComponent(props){
    // props : we pass the ticker id as ticker

    const dispatch = useDispatch();
    const portfolio_manager = useSelector(state => state.portfolio);


    const [starting_investment, setStartingInvestment] = React.useState(0);
    const [price, setPrice] = React.useState(0);

    const handleSubmit = () => {
        
        const data = {
            qty: 0,
            starting_value_of_ticker: price,
            starting_investment: starting_investment,
            ticker: props.ticker,
            portfolio: portfolio_manager.portfolio.id
        }
        console.log("data", data)
        // portfolioServices.create_user_ticker(data, dispatch);
        // props.closeWindow();
    }

    return (
        <div className="card">
            <div className="card-header">
                <h4> Add ticker</h4>
                <hr />
                <button onClick={()=> props.closeWindow()} className="btn btn-danger">Close</button>
            </div>

            <div className="card-body">
                <hr />
                <form  className="form">
                    <div className="form-group">
                        <label for="exampleInputEmail1">Invest</label>
                    
                        <input 
                            value={starting_investment} 
                            onChange={(e)=> setStartingInvestment(e.target.value)}
                            type="number" 
                            className="form-control"
                            style={{backgroundColor: "#ffca7b"}}
                            step="0.01"
                        />
                        <input 
                            value={price} 
                            onChange={(e)=> setPrice(e.target.value)}
                            type="number" 
                            className="form-control"
                            style={{backgroundColor: "#ffca7b"}}
                            step="0.01"
                        />
                    </div>
                    <br />
              
                    <button className="btn btn-primary" onClick={handleSubmit()}>Buy</button>
                </form>
            </div>
            
        </div>
    )


};