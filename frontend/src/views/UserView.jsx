import * as React from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import userService from "../data/services/authServices";
import NavbarComponent from "../components/navbar";
import TopNavbarComponent from "../components/TopNavbar";
import PortfolioListComponent from "../components/portfolios/PortfolioListComponent";


export default function UserView(){
    const dispatch = useDispatch();
    const user_manager = useSelector(state => state.user)
    const navigate = useNavigate();
    const isAuthenticated = user_manager.isAuthenticated;
    const user = user_manager.user;

    React.useEffect(()=>{
        if (isAuthenticated !== "true"){
            navigate("/login")
        }
    }, [isAuthenticated])

    React.useEffect(()=>{
        if (isAuthenticated === "true"){
            userService.current_user(dispatch)
        }
        
    }, [isAuthenticated])

    return (
        <div>
            <NavbarComponent />
            <main className="main-content border-radius-lg">
                <TopNavbarComponent />
                <div className="container-fluid py-4">
                    <div className="row">
                        <div className="col-4">
                            <div className="card">
                                <div className="card-header">
                                    <h4>{user.username}</h4>
                                </div>
                            </div>
                        </div>

                        <div className="col-8">
                            <div className="card">
                                <div className="card-header">
                                    <button className="btn btn-sucess">CREATE PORTFOLIO</button>
                                </div>
                                <div className="card-body">
                                    <PortfolioListComponent />
                                </div>
                            </div>
                            
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )
}