import * as React from "react";
import { useDispatch } from "react-redux";




export default AddTickerToPortfolioComponent(){
    const dispatch = useDispatch();

    const [starting_investment, setStartingInvestment] = React.useState(0);
    const qty = 0

    const handleSubmit = () => {
        const data = {
            qty: qty,
            starting_investment: starting_investment,
            ticker: 0,
            portfolio: 0
        }
    }

    return (
        <div className="card">
            <div className="card-header">
                <h4> Add ticker</h4>
                <hr />
                <button className="btn btn-danger">Close</button>
            </div>

            <div className="card-body">
                <form className="form">
                
                </form>
            </div>
            
        </div>
    )


}