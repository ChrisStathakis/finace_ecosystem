import * as React from "react";
import portfolioServices from "../../data/services/portfolioServices";
import { useDispatch } from "react-redux";



export default function PortfolioAddTickerComponent(props){
    const dispatch = useDispatch()
    const [starting_investment, setStartingInvestment] = React.useState(0);
    const [starting_value_of_ticker, setStartingValueOfTicker] = React.useState(0);
    const [current_value, setCurrentValue] = React.useState(0);

    const port = props.port;
    const ticker = props.ticker;

    React.useEffect(()=>{
        const ticker_ = props.ticker;
        setCurrentValue(ticker_.price);
        setStartingValueOfTicker(ticker_.price)
    }, [])



    const handleSubmit = (e) => {
        e.preventDefault();
        const data = {
            starting_investment: starting_investment,
            ticker: ticker.id,
            portfolio: port,
            qty: 0,
            starting_value_of_ticker: starting_value_of_ticker,
            current_value: current_value,
            is_sell: false,
            price: 0
        }
        
        portfolioServices.create_user_ticker(data, port, dispatch);
        props.handleClose()
    };



    return (
        <div className="card">
            <div className="card-header">
                <h4>Ticker</h4>
                <button onClick={props.handleClose} className="btn btn-warning">Close</button>
            </div>
            <div className="card-body">
                <form className="form">
                    <div className="row">
                        <div className="col-4"></div>
                        <div className="col-4">
                            <label>Starting Investment</label>
                            <input style={{backgroundColor: "#d7d7d8"}} onChange={(e)=> setStartingInvestment(e.target.value)} type="number" className="form-control" placeholder="Investment" value={starting_investment} name="starting_investment" />
                            <label>Starting Value</label>
                            <input style={{backgroundColor: "#d7d7d8"}} onChange={(e)=> setStartingValueOfTicker(e.target.value)} type="number" className="form-control"
                                placeholder="Starting Value" value={starting_value_of_ticker} name="starting_value"
                            />
                            <br />
                            <label>Current Value</label>
                            <input style={{backgroundColor: "#d7d7d8"}} onChange={(e)=> setCurrentValue(e.target.value)} type="number" className="form-control" placeholder="Current Value" value={current_value} name="current_value" />
                            <br />
                            <button className="btn btn-success" onClick={handleSubmit}>Save</button>
                        </div>
                    </div>
                    
                </form>
            </div>
        </div>
    )
}