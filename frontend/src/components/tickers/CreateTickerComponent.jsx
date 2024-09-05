import * as React from "react";
import tickerServices from "../../data/services/ticker.services";
import { useDispatch } from "react-redux";



export default function CreateTickerComponent(props){
    const [ticker, setTicker] = React.useState("");
    const [title, setTitle] = React.useState("");
    const [indices, setIndices] = React.useState("");

    const dispatch = useDispatch();

    const handleSubmit = () => {
        const data = {
            title,
            ticker,
            indices
        }
        tickerServices.createTicker(data, dispatch);
        props.closeWindow();
    }

    return (
        <div className="row">
            <div className="col-4"></div>
            <div className="col-4">
                <div className="card">
                    <div className="card-header">
                        <h4>CREATE TICKER</h4>
                        <button className="btn btn-warning" onClick={()=> props.closeWindow()}>Close</button>
                    </div>
                    <div className="card-body">
                        <form className="form">

                            <div class="form-group">
                                <label for="title">TITLE</label>
                                <input type="text" value={title} onChange={(e)=> setTitle} className="form-control" id="title" placeholder="Enter Title" />   
                            </div>

                            <div class="form-group">
                                <label for="code">CODE</label>
                                <input type="text" className="form-control" id="code" placeholder="Enter Title" />   
                            </div>

                            <button className="btn btn-success">Save</button>
                        </form>
                    </div>
                </div>
            </div>

        </div>
    )




}