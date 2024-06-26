import * as React from "react";
import { useDispatch, useSelector } from "react-redux";
import rssSevices from "../../data/services/rss.sevices";




export default function RssListComponent(props) {
    
    const dispatch = useDispatch();
    const rss_manager = useSelector(state => state.rss);
    const rss_list = rss_manager.rss_list;
    
    React.useEffect(()=>{
        rssSevices.fetch_rss_list("", dispatch);
    }, [])

    const handleChange = (id) => {
        rssSevices.fetch_rss_detail(id, dispatch)
        props.handleButton();
    }

    return (
        <div className="container-fluid py-4">
            <div className="row">
                <h4>Rss Feed</h4>
                <div className="co-8">
                    <table className="table table-bordered">
                        <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Title</th>
                                    <th>Positive</th>
                                    <th>Analysis</th>
                                    <th>-</th>
                                </tr>
                            </thead>
                            <tbody>
                                {rss_list.results.map((rss)=>{
                                    return (
                                        <tr>
                                            <td >{rss.id}</td>
                                            <td style={{alignContent:"left"}}>{rss.title}</td>
                                            <td></td>
                                            <td></td>
                                            <td><btn onClick={()=> handleChange(rss.id)} className="btn btn-info">Details</btn></td>
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