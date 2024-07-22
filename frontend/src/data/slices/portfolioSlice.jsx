import { createSlice } from "@reduxjs/toolkit";
import { PORTFOLIO_ID } from "../actionTypes";


const initialState = {
    portfolios: [],
    port_detail: {},
    port_tickers: [],
    portfolio_id: localStorage.getItem(PORTFOLIO_ID)
    
}


const portfolioSlice = createSlice({
    name: "portfolio",
    initialState,
    reducers: {
        fetch_portfolios_action: (state, action) => {
            state.portfolios = action.payload.results;
        },
        fetch_portfolio_action: (state, action)=>{
            state.port_detail = action.payload
        },
        fetch_port_tickers_action: (state, action) => {
            state.port_tickers = action.payload.results
        },
        create_portfolio_action: (state, action) => {
            state.portfolios = [action.payload, ...state.portfolios]
        },
        create_port_ticker_action: (state, action) => {
            state.port_tickers = [action.payload, ...state.port_tickers]
        },
        update_port_ticker_action: (state, action) => {
            state.port_detail = action.payload;
        },
        selectPortfolioAction: (state, action) => {
            state.portfolio_id = action.payload;
            localStorage.setItem(PORTFOLIO_ID, action.payload);
        }
        
    }
});

export const {
    fetch_port_tickers_action, fetch_portfolio_action, fetch_portfolios_action, create_portfolio_action, 
    create_port_ticker_action, update_port_ticker_action, selectPortfolioAction
} = portfolioSlice.actions;

export default portfolioSlice.reducer;