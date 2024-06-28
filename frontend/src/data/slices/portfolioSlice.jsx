import { createSlice } from "@reduxjs/toolkit";


const initialState = {
    portfolios: [],
    port_detail: {},
    port_tickers: []
    
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
        
    }
});

export const {
    fetch_port_tickers_action, fetch_portfolio_action, fetch_portfolios_action, create_portfolio_action, 
    create_port_ticker_action 
} = portfolioSlice.actions;

export default portfolioSlice.reducer;