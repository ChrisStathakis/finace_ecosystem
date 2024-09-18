import React from "react";
import tickerServices from "../../data/services/ticker.services";
import { useDispatch } from "react-redux";


export function CreateTickerComponent(props){
    const dispatch = useDispatch();
    const [ticker, setTicker] = React.useState("");
    const [title, setTitle] = React.useState("");


    const handleData = (e) => {
        e.preventDefault();
        const data = {
            ticker,
            title,
            indices: "^GSPC"
        }
        tickerServices.create_ticker(data, dispatch);
        props.closeWindow();
    };


    return (

        <div className="container-fluid py-4">
            <div className="row">
                <div className="col-4"></div>
                <div className="col-4">
                    <div className="card">
                        <div className="card-header">
                            <h4>CREATE A TICKER</h4>
                            <button onClick={() => props.closeWindow()} className="btn btn-warning">Close</button>
                        </div>

                        <div className="card-body">
                            <form className="form">
                                <div class="form-group">
                                    <label for="ticker_label">Ticker</label>
                                    <input type="text" className="form-control" id="ticker_label" placeholder="Enter Title" value={title} onChange={(e => setTitle(e.target.value))} />
                                </div>

                                <div class="form-group">
                                    <label for="code_label">CODE</label>
                                    <input type="text" className="form-control" id="code_label" placeholder="Enter Title" value={ticker} onChange={(e => setTicker(e.target.value))} />
                                </div>

                                <button onClick={(e) => handleData(e)} className="btn btn-success" type="submit">Save</button>

                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )



}