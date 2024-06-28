import axiosInstance from "../axiosInstance";
import { PORTFOLIO_DETAIL_ENDPOINT, PORTFOLIO_LIST_ENDPOINT, USER_TICKERS_LIST_ENDPOINT } from "../endpoints";
import { create_portfolio_action, fetch_port_tickers_action, fetch_portfolio_action, fetch_portfolios_action } from "../slices/portfolioSlice";




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
    const endpoint = `${PORTFOLIO_DETAIL_ENDPOINT}/${id}/`;
    axiosInstance.get(endpoint)
        .then(
            (response)=>{
                dispatch(fetch_portfolio_action(response.data));
            }
        )

};

function fetch_user_tickers(id, dispatch){
    const endpoint = `${USER_TICKERS_LIST_ENDPOINT}?portfolio=${id}`;
    axiosInstance.get(endpoint)
        .then(
            (response)=>{
                dispatch(fetch_port_tickers_action(response.data));
            }
        )
}


export default {
    fetch_portfolio,
    fetch_portfolios,
    createPortfolio,
    fetch_user_tickers
}