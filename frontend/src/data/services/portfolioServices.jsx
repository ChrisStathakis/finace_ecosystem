import axiosInstance from "../axiosInstance";
import { PORTFOLIO_DETAIL_ENDPOINT, PORTFOLIO_LIST_ENDPOINT, USER_TICKERS_LIST_ENDPOINT, USER_TICKER_CREATE_ENDPOINT, USER_TICKER_DELETE_ENDPOINT, USER_TICKER_DETAIL_ENDPOINT, USER_TICKER_UPDATE_ENDPOINT } from "../endpoints";
import { create_port_ticker_action, create_portfolio_action, fetch_port_tickers_action, fetch_portfolio_action,
         fetch_portfolios_action, selectPortfolioAction, update_port_ticker_action, fetch_all_user_tickers_action
 } from "../slices/portfolioSlice";




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
    // backend is resposible to send only the instances is owned
    const endpoint = `${USER_TICKERS_LIST_ENDPOINT}?portfolio=${id}`;
    axiosInstance.get(endpoint)
        .then(
            (response)=>{
                dispatch(fetch_port_tickers_action(response.data));
            }
        )
};

function fetch_all_user_tickers(dispatch){
    // backend is resposible to send only the instances is owned
    axiosInstance.get(USER_TICKERS_LIST_ENDPOINT)
        .then(
            (response) => {
                dispatch(fetch_all_user_tickers_action(response.data))
            }
        )
}

function fetch_user_active_tickers(id, dispatch){
    const endpoint = `${USER_TICKERS_LIST_ENDPOINT}?portfolio=${id}&is_sell=false`;
    axiosInstance.get(endpoint)
        .then(
            (response)=>{
                dispatch(fetch_port_tickers_action(response.data));
            }
        )
};

function create_user_ticker(data, dispatch){
    axiosInstance.post(USER_TICKER_CREATE_ENDPOINT, data).then(
        (response)=>{
            dispatch(create_port_ticker_action(response.data))
        }
    )
}

function edit_user_ticker(data, dispatch) {
    console.log("Begins")
    console.log(data);
    console.log(data.id)
    const endpoint = `${USER_TICKER_UPDATE_ENDPOINT}/${data["id"]}/`;
    
    console.log(endpoint);
    axiosInstance.put(endpoint, data)
        .then(
            (response) => {
                dispatch(update_port_ticker_action(response.data))
                fetch_portfolio(data.portfolio, dispatch);
            }
        )
};

function delete_user_ticker(id, port_id, dispatch){
    const endpoint =  `${USER_TICKER_DELETE_ENDPOINT}/${id}/`;
    axiosInstance.delete(endpoint)
        .then(
            (resp) => {
                fetch_portfolio(port_id, dispatch);
                fetch_user_tickers(port_id, dispatch);
            }
        )
}

function select_portfolio(port_id, dispatch){
    dispatch(selectPortfolioAction(port_id))
}


export default {
    fetch_portfolio,
    fetch_portfolios,
    createPortfolio,
    fetch_user_tickers,
    create_user_ticker,
    edit_user_ticker,
    select_portfolio,
    fetch_user_active_tickers,
    delete_user_ticker,
    fetch_all_user_tickers
}