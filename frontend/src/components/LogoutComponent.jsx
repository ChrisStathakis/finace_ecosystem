import * as React from "react";
import {useDispatch} from "react-redux";
import userService from '../data/services/authServices';


export default function LogoutComponent(){
    const dispatch = useDispatch();


    React.useEffect(()=>{
        userService.logout(dispatch)
    }, [])

    return (
        <div>
            <>Logout</>
        </div>
    )


}