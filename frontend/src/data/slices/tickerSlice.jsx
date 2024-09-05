import {createSlice } from "@reduxjs/toolkit";



const initialState = {
    tickers: {
        count: 0,
        next: "",
        previous: "",
        results: []
    },
    selectedTicker: {},
    selectedTickerID: 0,
    isLoaded: false,
    tickerDataframe: [],
    rss_feed: {
        count: 0,
        next: "",
        previous: "",
        results: []
    },
    main_page_tickers: []
}


const tickerSlice = createSlice({
    name: "tickers",
    initialState,
    reducers: {
        fetch_tickers_action: (state, action) => {
            const tickers = action.payload;
            state.tickers = tickers;
        },
        fetch_ticker_action: (state, action) => {
            state.selectedTicker = action.payload;
            state.selectedTickerID = action.payload.id
        },
        fetch_ticker_dataframe_action: (state, action) => {
            state.tickerDataframe = action.payload.results;
        },
        fetch_rss_feed_action: (state, action) => {
            state.rss_feed = action.payload;
        },
        fetch_main_page_tickers_action: (state, action) => {
            console.log(action.payload);
            state.main_page_tickers = action.payload.results;
        },
        create_ticker_action: (state, action) =>{
            state.tickers = [...state.tickers, action.payload];
        }
    }
});


export const { fetch_tickers_action, fetch_ticker_action, fetch_ticker_dataframe_action,
     fetch_rss_feed_action, fetch_main_page_tickers_action, create_ticker_action

    } = tickerSlice.actions;
export default tickerSlice.reducer;