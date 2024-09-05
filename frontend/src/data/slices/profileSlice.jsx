import { createSlice } from "@reduxjs/toolkit";
import { PORTFOLIO_ID } from "../actionTypes";


const initialState = {
    starting_value: 0,
    current_value: 0,
    withdraw_value: 0,
    historic_value: 0,
    portfolio_id: localStorage.getItem(PORTFOLIO_ID)
}


const profileSlice = createSlice({
    name: "profile",
    initialState,
    reducers: {
        fetch_profile_action: (state, action) => {
            
            state.starting_value = action.payload.starting_value;
            state.current_value = action.payload.current_value;
            state.withdraw_value = action.payload.withdraw_value;
            state.historic_value = action.payload.historic_value;
            state.portfolio_id = action.payload.portfolio_id;
            localStorage.setItem(PORTFOLIO_ID, action.payload.portfolio_id);
        }
    }

});


export const {
    fetch_profile_action
} = profileSlice.actions;

export default profileSlice.reducer