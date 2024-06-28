import * as React from "react";
import { useDispatch, useSelector } from "react-redux";

import portfolioServices from "../../data/services/portfolioServices";


export default function AddTickerToPortfolioComponent(props){
    const dispatch = useDispatch();
    const portfolio_manager = useSelector(state => state.portfolio);


    const [starting_investment, setStartingInvestment] = React.useState(0);
    const qty = 0

    const handleSubmit = () => {
        const data = {
            qty: qty,
            starting_investment: starting_investment,
            ticker: props.ticker,
            portfolio: portfolio_manager.portfolio.id
        }
        portfolioServices.create_user_ticker(data, dispatch);
        props.closeWindow();
    }

    return (
        <div className="card">
            <div className="card-header">
                <h4> Add ticker</h4>
                <hr />
                <button onClick={()=> props.closeWindow()} className="btn btn-danger">Close</button>
            </div>

            <div className="card-body">
                <form className="form ustify-content-center align-items-center">
                
                    <h5>Add the invest</h5>
                    <br />
                    <input 
                        value={starting_investment} 
                        onChange={(e)=> setStartingInvestment(e.target.value)}
                        type="number" 
                        className="form-control"
                        style={{maxWidth:"30%", paddingLeft:"10%"}}
                        step="0.01"
                    />
                    
              
                    
                    <button className="btn btn-primary" onClick={handleSubmit}>Buy</button>
                </form>
            </div>
            
        </div>
    )


}