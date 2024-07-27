import { createSlice } from "@reduxjs/toolkit";
import {IS_AUTHENTICATED, ACCESS_TOKEN, REFRESH_TOKEN } from "../actionTypes";


const initialState = {
    user: {
        "id": 0,
        "username": "",
    },
    accessToken: localStorage.getItem(ACCESS_TOKEN, ""),
    refreshToken: localStorage.getItem(REFRESH_TOKEN, ""),
    isAuthenticated: localStorage.getItem(IS_AUTHENTICATED, "false")
}


const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {
        login_action: (state, action) => {
            state.accessToken = action.payload.access;
            state.refreshToken = action.payload.refresh;
            state.isAuthenticated = "true";
        },
        logout_action: (state, action) => {
            state.refreshToken = "";
            state.accessToken = "";
            state.isAuthenticated = "false";
            localStorage.setItem(IS_AUTHENTICATED, "false")
        },
        user_action: (state, action) => {
            state.user = action.payload;
            
        }
    }
});



export const {login_action, logout_action, user_action} = userSlice.actions;
export default userSlice.reducer;