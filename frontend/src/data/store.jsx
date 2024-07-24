import { configureStore, combineReducers } from "@reduxjs/toolkit";

import tickerSlice from "./slices/tickerSlice";
import searchSlice from "./slices/searchSlice";
import rssSlice from "./slices/rssSlice";
import userSlice from "./slices/userSlice";
import portfolioSlice from "./slices/portfolioSlice";
import profileSlice from "./slices/profileSlice";


const store = configureStore({
    reducer: {
        tickers: tickerSlice,
        search: searchSlice,
        rss: rssSlice,
        user: userSlice,
        portfolio: portfolioSlice,
        profile: profileSlice
    }
})


export default store;