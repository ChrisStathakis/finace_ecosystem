import * as React from "react";
import portfolioServices from "../../data/services/portfolioServices";
import { useDispatch } from "react-redux";



export default function PortfolioAddTickerComponent(props){
    const dispatch = useDispatch()
    const [starting_investment, setStartingInvestment] = React.useState(0);
    const [current_value, setCurrentValue] = React.useState(0);

    const port = props.port;
    const ticker = props.ticker;
    React.useEffect(()=>{
        
    }, [])

    const handleSubmit = () => {
        const data = {
            starting_investment: starting_investment,
            current_value: current_value,
            portfolio: port,
            ticker: ticker
        }
        portfolioServices.create_user_ticker(data, dispatch)
    }

    return (
        <div className="card">
            <div className="card-header">
                <h4>Ticker</h4>
                <button className="btn btn-warning"><CLOSE></CLOSE></button>
            </div>
            <div className="card-body">
                <form className="form">
                    <input onChange={(e)=> setStartingInvestment(e.target.value)} type="number" className="form-control" placeholder="Investment" value={current_value} name="starting_investment" />
                    <input onChange={(e)=> setCurrentValue(e.target.value)} type="number" className="form-control" placeholder="Starting Value" value={current_value} name="current_value" />
                </form>
            </div>
        </div>
    )
}