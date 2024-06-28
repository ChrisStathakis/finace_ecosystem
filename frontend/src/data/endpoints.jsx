export const BASE_URL = "http://127.0.0.1:8000/api/";

export const ACCESS_TOKEN_ENDPOINT = BASE_URL +  "token/";
export const REFRESH_TOKEN_ENDPOINT = BASE_URL +  "token/refresh/";
export const CURRENT_USER_ENDPOINT = BASE_URL + "current-user/";


export const TICKERS_LIST_ENDPOINT = BASE_URL +  "tickers/tickers/list/";
export const TICKER_DETAIL_ENDPOINT = BASE_URL + "tickers/detail";
export const TICKER_DATAFRAME_ENDPOINT = BASE_URL + "tickers/tickers/dataframe/";
export const RSS_FEED_TICKER_ENDPOINT = BASE_URL + "rss-feed/";
export const RSS_FEED_DETAIL_ENDPOINT = BASE_URL + "rss-feed/detail";


export const PORTFOLIO_LIST_ENDPOINT = BASE_URL + "tickers/portfolios/list/";
export const PORTFOLIO_DETAIL_ENDPOINT = BASE_URL + "tickers/portfolio/detail";
export const USER_TICKERS_LIST_ENDPOINT = BASE_URL + "tickers/user-tickers/list/";
export const USER_TICKER_DETAIL_ENDPOINT = BASE_URL + "tickers/user-tickers/detail";
export const PREDICT_TICKER_ENDPOINT = BASE_URL + "tickers/tickers/prediction";