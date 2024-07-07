import * as React from "react";
import { useSelector, useDispatch } from "react-redux";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
import { Line } from 'react-chartjs-2';
import tickerServices from "../../data/services/ticker.services";
import axiosInstance from "../../data/axiosInstance";
import axios from "axios";
import { PREDICT_TICKER_ENDPOINT } from "../../data/endpoints";


ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

export const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top'
      },
      title: {
        display: true,
        text: 'Chart.js Line Chart',
      },
    },
};




export default function TickerDetailComponent(props){
    const [predict, setPredict] = React.useState(0);

    const tickerManager = useSelector(state => state.tickers);
    const dispatch = useDispatch();

    const ticker = tickerManager.selectedTicker;
    const tickerID = tickerManager.selectedTickerID;
    const tickerDataframe = tickerManager.tickerDataframe;
    const rss_feed = tickerManager.rss_feed;

    let labels = [];
    let values = []

    React.useEffect(()=>{
        tickerServices.fetchTickerDataframe(tickerID, dispatch);
        tickerServices.fetchRssFeed(tickerID, dispatch);

    }, [tickerID])


    React.useEffect(()=>{
        for (let i = 0; i < tickerDataframe.length; i++) {
            const row = tickerDataframe[i];
            labels.push(row.date)
            values.push(row.close);
        }
    }, [tickerDataframe])

    
    const data = {
        labels,
        datasets: [
        {
            label: 'Dataset 1',
            data: values,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
        }
        ],
    };
    
   

    return(
        <div className="container-fluid py-4">
            <div className="row">
                <div className="col-8">
                    <div style={{maxHeight:"5%"}} className="card">
                        <div className="card-header"><h4>{ticker.title}</h4></div>
                       
                    </div>
                </div>
                <div className="col-4">
                    <div style={{maxHeight:"5%"}} className="card">
                        <div className="card-header"><button onClick={props.closeWindow} className="btn btn-secondary">Back</button></div>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-8">
                    <Line options={options} data={data} />
                </div>
                <div className="col-4">
                    <h5>Prices</h5>
                    <table className="table table-bordered">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Price</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tickerDataframe.map((ele)=> {
                                    return (
                                        <tr>
                                            <td>{ele.date}</td>
                                            <td>{ele.close}</td>
                                        </tr>
                                    )
                                })
                            }
                        </tbody>
                    </table>
                </div>
            </div>
            <div className="row">
                <div className="col-4">
                    <h4>{ticker.title}</h4>
                    <p>Details</p>
                    <table className="table table-bordered">
                        <thead>
                            <tr>
                                <th>Beta</th>
                                <th>{ticker.beta}</th>
                            </tr>
                            <tr>
                                <th>Coverage</th>
                                <th>{ticker.coverage}</th>
                            </tr>
                            <tr>
                                <th>Market Variance</th>
                                <th>{ticker.market_variance}</th>
                            </tr>
                            <tr>
                                <th>Camp</th>
                                <th>{ticker.camp}</th>
                            </tr>
                            <tr>
                                <th>Standard Deviation</th>
                                <th>{ticker.standard_deviation}</th>
                            </tr>
                            

                        </thead>
                    </table>
                </div>
                <div className="col-4">
                    <h4>Prices</h4>
                    <br />
                    <table className="table table-bordered">
                        <thead>
                            <tr>
                                <th>Price</th>
                                <th>{ticker.price}</th>
                            </tr>
                            <tr>
                                <th>Simply Return</th>
                                <th>{ticker.simply_return} % </th>
                            </tr>
                            <tr>
                                <th>Log Return</th>
                                <th>{ticker.log_return} %</th>
                            </tr>
                            <tr>
                                <th>Predict</th>
                                <th>{predict}</th>
                            </tr>
                 
                        </thead>
                    </table>
                </div>
                <div className="col-4">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Date</th>
                                <td>Title</td>
                                <td>Positive</td>
                            </tr>
                        </thead>
                        <tbody>
                            {rss_feed.results.map((ele)=>{
                                return (
                                    <tr>
                                        <td>{ele.id}</td>
                                        <td></td>
                                        <td></td>
                                        <td></td>
                                    </tr>
                                )
                            })}
                            
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )


}