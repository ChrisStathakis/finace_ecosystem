import * as React from "react";
import { useDispatch, useSelector } from "react-redux";
import {useNavigate } from 'react-router-dom';
import userService from "../data/services/authServices";



export default function LoginView(){
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");

    const user_manager = useSelector(state=>state.user);
    const isAuthenticated = user_manager.isAuthenticated;

    React.useEffect(()=>{
        console.log("is Authenticated", isAuthenticated)
        if (isAuthenticated === "true"){
                navigate("/")
        }
    }, [isAuthenticated])

    const handleLogin = (e) => {
        e.preventDefault();
        userService.login(username, password, dispatch);
    };

  



    return (
        <div>
            <div className="row">
                <div className="col-4"></div>
                <div className="col-4">
                    <div className="card">
                        <div className="card-header">
                            <h4>Login</h4>
                        </div>
                        <div className="card-body">
                            <form className="form">
                                <input type="text" onChange={(e)=>setUsername(e.target.value)} value={username} className="form-control" placeholder="Username" />
                                <input type="password" onChange={(e)=>setPassword(e.target.value)} value={password} className="form-control" placeholder="Password" />
                                <button className="btn btn-success" onClick={(e) => handleLogin(e)}>Login</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}