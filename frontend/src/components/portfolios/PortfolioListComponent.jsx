import * as React from "react";
import {useDispatch, useSelector} from "react-redux";
import portfolioServices from "../../data/services/portfolioServices";


export default function PortfolioListComponent(){
    const dispatch = useDispatch()
    const portfolio_manager = useSelector(state => state.portfolio)
    const { portfolios } = portfolio_manager

    React.useEffect(()=>{
        portfolioServices.fetch_portfolios(dispatch);
    },[])

    return (
        <table className="table table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                </tr>
            </thead>
            <tbody>
                {portfolios.map((ele)=>{
                    return (
                        <tr>
                            <td>{ele.id}</td>
                            <td>{ele.title}</td>
                        </tr>
                    )
                })}
            </tbody>
        </table>
    )


}