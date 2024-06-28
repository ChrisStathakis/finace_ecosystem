import * as React from "react";
import {useDispatch, useSelector} from "react-redux";
import portfolioServices from "../../data/services/portfolioServices";


export default function PortfolioListComponent(props){
    const dispatch = useDispatch()
    const portfolio_manager = useSelector(state => state.portfolio)
    const { portfolios } = portfolio_manager

    React.useEffect(()=>{
        portfolioServices.fetch_portfolios(dispatch);
    },[])

    const handleSelectedPortfolio = (id) => {
        portfolioServices.fetch_portfolio(id, dispatch);
        props.showDetail()
    }

    return (
        <table className="table table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {portfolios.map((ele)=>{
                    return (
                        <tr>
                            <td>{ele.id}</td>
                            <td>{ele.title}</td>
                            <td><button onClick={() => handleSelectedPortfolio(ele.id)} className="btn btn-info">More</button></td>
                        </tr>
                    )
                })}
            </tbody>
        </table>
    )


}