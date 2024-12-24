import { createSlice } from "@reduxjs/toolkit";
import { PORTFOLIO_ID } from "../actionTypes";


const initialState = {
    starting_value: 0,
    current_value: 0,
    starting_withdraw_value: 0,
    withdraw_value:0,
    historic_withdraw_value:0,
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
            state.starting_withdraw_value = action.payload.starting_withdraw_value;
            state.withdraw_value = action.payload.withdraw_value;
            state.historic_withdraw_value = action.payload.historic_withdraw_value;
            state.historic_value = action.payload.historic_value;
            state.earnings = action.payload.earnings;
            state.withdraw_earnings = action.payload.withdraw_earnings;
            state.historic_earnings = action.payload.historic_earnings;
            state.portfolio_id = action.payload.portfolio_id;
            localStorage.setItem(PORTFOLIO_ID, action.payload.portfolio_id);
        }
    }

});


export const {
    fetch_profile_action
} = profileSlice.actions;

export default profileSlice.reducer