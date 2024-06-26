import { configureStore, combineReducers } from "@reduxjs/toolkit";

import tickerSlice from "./slices/tickerSlice";
import searchSlice from "./slices/searchSlice";
import rssSlice from "./slices/rssSlice";
import userSlice from "./slices/userSlice";
import portfolioSlice from "./slices/portfolioSlice";

const store = configureStore({
    reducer: {
        tickers: tickerSlice,
        search: searchSlice,
        rss: rssSlice,
        user: userSlice,
        portfolio: portfolioSlice
    }
})


export default store;