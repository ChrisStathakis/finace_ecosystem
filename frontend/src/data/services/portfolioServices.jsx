import axiosInstance from "../axiosInstance";
import { PORTFOLIO_LIST_ENDPOINT } from "../endpoints";
import { create_portfolio_action, fetch_portfolios_action } from "../slices/portfolioSlice";




function createPortfolio(data, dispatch){
    axiosInstance.post(PORTFOLIO_LIST_ENDPOINT, data)
        .then(
            (response) => {
                dispatch(create_portfolio_action(response.data))
            }
        )
};


function fetch_portfolios(dispatch){
    axiosInstance.get(PORTFOLIO_LIST_ENDPOINT)
        .then(
            (response) => {
                console.log("response portfolio", response.data)
                dispatch(fetch_portfolios_action(response.data));
            }
        )
};


function fetch_portfolio(id, dispatch){
    
};


export default {
    fetch_portfolio,
    fetch_portfolios,
    createPortfolio
}