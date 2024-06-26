import { createSlice } from "@reduxjs/toolkit";


const initialState = {
    rss_list: {
        count: 0,
        next: "",
        previous: "",
        results: []
    },
    rss_detail: {}
}



const rssSlice = createSlice({
    name: "rss",
    initialState,
    reducers: {
        fetch_rss_list_action: (state, action) => {
            state.rss_list = action.payload;
        },
        fetch_rss_detail_action: (state, action) => {
            state.rss_detail = action.payload
        }
    }
});


export const { fetch_rss_list_action, fetch_rss_detail_action  } = rssSlice.actions;
export default rssSlice.reducer;