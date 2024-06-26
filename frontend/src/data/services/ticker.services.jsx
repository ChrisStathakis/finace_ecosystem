import axios from "axios";

import { RSS_FEED_TICKER_ENDPOINT, TICKERS_LIST_ENDPOINT, TICKER_DATAFRAME_ENDPOINT, TICKER_DETAIL_ENDPOINT } from "../endpoints";
import { fetch_rss_feed_action, fetch_ticker_action, fetch_ticker_dataframe_action, fetch_tickers_action } from "../slices/tickerSlice";


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

const fetchTickerDataframe = (id, dispatch) => {
    const endpoint = `${TICKER_DATAFRAME_ENDPOINT}?ticker=${id}`;
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
}


export default {
    fetchTickers,
    fetchTicker,
    fetchTickerDataframe,
    fetchRssFeed
}