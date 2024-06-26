import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    q: "",
    searchTickers: false,
    searchRss: false
}


const searchSlice = createSlice({
    name: "search",
    initialState,
    reducers: {
        search_tickers_action: (state, action) => {
            state.q = action.payload;
            state.searchTickers = true;
            state.searchRss = false
        }
    }
});

export const {search_tickers_action} = searchSlice.actions;
export default searchSlice.reducer;