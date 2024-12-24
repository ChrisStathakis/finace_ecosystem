import * as React from "react";
import { useDispatch, useSelector } from "react-redux";
import portfolioServices from "../../data/services/portfolioServices";



export default function UserTickerListComponent(props){
    const dispatch = useDispatch();

    const portManager = useSelector(state=> state.portfolio); 
    const all_tickers = portManager.all_tickers;

    React.useEffect(()=>{
        portfolioServices.fetch_all_user_tickers(dispatch);
    },[])

    return (
        <div className="container-fluid py-4">
            <div className="table-responsible p-0">
                <div className="table align-items-lg-center mb-0">
                    <thead>
                        <tr>
                            <th className="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Date</th>
                            <th className="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Ticker</th>
                            <th className="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Starting Value</th>
                            <th className="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Investment</th>
                            <th className="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Current/Sale Value</th>
                            <th className="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Earnings</th>
                            <th className="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {all_tickers.map((ele)=>{
                            return (
                                <tr>
                                    <td>{ele.timestamp}</td>
                                    <td>{ele.title}</td>
                                    <td>{ele.starting_investment}</td>
                                    <td>{ele.qty}</td>
                                    <td>{ele.current_value}</td>
                                    <td>{ele.difference} / {ele.diff_percent} %</td>
                                    <td>{ele.ticker_status}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </div>
            </div>
        </div>
    )

}