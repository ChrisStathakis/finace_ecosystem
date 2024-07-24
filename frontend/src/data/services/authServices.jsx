import axios from "axios";
import { ACCESS_TOKEN_ENDPOINT, CURRENT_USER_ENDPOINT, PROFILE_ENDPOINT } from "../endpoints";
import { login_action, user_action } from "../slices/userSlice";
import { ACCESS_TOKEN, REFRESH_TOKEN, IS_AUTHENTICATED } from "../actionTypes";
import axiosInstance from "../axiosInstance.jsx";
import { fetch_profile_action } from "../slices/profileSlice.jsx";




function login(username, password, dispatch){
    const data = {username: username, password: password};
    axios.post(ACCESS_TOKEN_ENDPOINT, data)
        .then(
            (response) => {
                console.log("result", response)
                const results = response.data;
                localStorage.setItem(ACCESS_TOKEN, results.access);
                localStorage.setItem(REFRESH_TOKEN, results.refresh);
                localStorage.setItem(IS_AUTHENTICATED, "true")
                dispatch(login_action(results));
            }
        )
}


function logout(dispatch){
    localStorage.setItem(ACCESS_TOKEN, "");
    localStorage.setItem(REFRESH_TOKEN, "");
    localStorage.setItem(IS_AUTHENTICATED, "false")
    
}

function current_user(dispatch){
    axiosInstance.get(CURRENT_USER_ENDPOINT)
        .then(
            (response)=>{
                dispatch(user_action(response.data))
            }
        )
};

function profile(dispatch){
    axiosInstance.get(PROFILE_ENDPOINT)
        .then(
            (response) => {
                dispatch(fetch_profile_action(response.data))
            }
        )
}


export default {
    login,
    logout,
    current_user,
    profile
}