import {search_tickers_action} from "../slices/searchSlice";



const search_tickers = (q, dispatch) => {
    dispatch(search_tickers_action(q));
};



export default {
    search_tickers

};