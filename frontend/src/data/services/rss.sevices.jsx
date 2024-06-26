import axios  from "axios";
import { RSS_FEED_DETAIL_ENDPOINT, RSS_FEED_TICKER_ENDPOINT } from "../endpoints";
import { fetch_rss_detail_action, fetch_rss_list_action } from "../slices/rssSlice";



const fetch_rss_list = (q="", dispatch) => {

    let endpoint =  `${RSS_FEED_TICKER_ENDPOINT}`;
    if (q.length > 1) { endpoint =`${endpoint}?search=${q}`};
    axios.get(endpoint)
        .then(
            (response)=> {
                dispatch(fetch_rss_list_action(response.data));
            }
        )
};


const fetch_rss_detail = (id, dispatch) => {
    const endpoint = `${RSS_FEED_DETAIL_ENDPOINT}/${id}/`;

    axios.get(endpoint)
        .then(
            (response)=>{
                dispatch(fetch_rss_detail_action(response.data))
            }
        )
};

export default {
    fetch_rss_detail,
    fetch_rss_list
}