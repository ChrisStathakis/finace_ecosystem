import { createSlice } from "@reduxjs/toolkit";


const initialState = {
    starting_value: 0,
    current_value: 0,
    withdraw_value: 0,
    historic_value: 0
}


const profileSlice = createSlice({
    name: "profile",
    initialState,
    reducers: {
        fetch_profile_action: (state, action) => {
            
            state.starting_value = action.payload.starting_value;
            state.current_value = action.payload.current_value;
            state.withdraw_value = action.payload.withdraw_value;
            state.historic_value = action.payload.historic_value
        }
    }

});


export const {
    fetch_profile_action
} = profileSlice.actions;

export default profileSlice.reducer