import axios from "axios";

import { PREDICT_TICKER_ENDPOINT, RSS_FEED_TICKER_ENDPOINT, TICKERS_LIST_ENDPOINT, TICKER_CREATE_ENDPOINT, TICKER_DATAFRAME_ENDPOINT, TICKER_DETAIL_ENDPOINT } from "../endpoints";
import { fetch_rss_feed_action, fetch_ticker_action, fetch_ticker_dataframe_action, fetch_tickers_action, fetch_main_page_tickers_action, create_ticker_action } from "../slices/tickerSlice";
import axiosInstance from "../axiosInstance";


const fetchTickers = (q="", dispatch) => {
    let endpoint = TICKERS_LIST_ENDPOINT;
    if (q.length > 1 ) {
        endpoint = `${endpoint}?search=${q}`;
    };
    console.log()
    axios.get(endpoint)
        .then(
            (response)=>{
                dispatch(fetch_tickers_action(response.data));
        })
    }


const fetchTicker = (id, dispatch) => {
    const endpoint = `${TICKER_DETAIL_ENDPOINT}/${id}/`;
    axios.get(endpoint)
        .then(
            (response)=> {
                dispatch(fetch_ticker_action(response.data));
            }
        )
};

export const createTicker = (data, dispatch) => {
    const endpoint = TICKER_CREATE_ENDPOINT;
    axiosInstance.post(endpoint, data)
        .then(
            (response)=>{
                dispatch(create_ticker_action(response.data));
            }
        )
}

const fetchTickerDataframe = (id, dispatch) => {
    const endpoint = `${TICKER_DATAFRAME_ENDPOINT}?ticker=${id}`;
    console.log("ticker datafame", endpoint)
    axios.get(endpoint)
        .then(
            (response) => {
                dispatch(fetch_ticker_dataframe_action(response.data));
                
            }
        )
}


const fetchRssFeed = (id, dispatch) => {
    const endpoint = `${RSS_FEED_TICKER_ENDPOINT}?ticker=${id}`;
    axios.get(endpoint)
        .then(
            (response)=> {
                dispatch(fetch_rss_feed_action(response.data));
            }
        )
};

const fetchPredictTicker = (id) => {
    const endpoint = `${PREDICT_TICKER_ENDPOINT}/${id}/`;
    axios.get(endpoint).then(
        (response) => {
            return response.data.my_predict;
        }
    )
};

const fetch_main_page_tickers = (dispatch) => {
    const endpoint = `${TICKERS_LIST_ENDPOINT}?ordering=-simply_return`;
    axios.get(endpoint).then(
        (response)=>{
            dispatch(fetch_main_page_tickers_action(response.data));
        }
    )
}


export default {
    fetchTickers,
    fetchTicker,
    fetchTickerDataframe,
    fetchRssFeed,
    fetchPredictTicker,
    fetch_main_page_tickers,
    createTicker
    
}