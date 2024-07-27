import * as React from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";

import portfolioServices from "../data/services/portfolioServices";
import userService from "../data/services/authServices";
import NavbarComponent from "../components/navbar";
import TopNavbarComponent from "../components/TopNavbar";
import PortfolioListComponent from "../components/portfolios/PortfolioListComponent";
import PortfolioCreateComponent from "../components/portfolios/PortofolioCreateComponent";
import PortfolioDetailComponent from "../components/portfolios/PortfolioDetailComponent";
import authServices from "../data/services/authServices";

export default function UserView(){
    const [showList, setShowList] = React.useState(true);
    const [showDetail, setShowDetail] = React.useState(false);
    
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const user_manager = useSelector(state => state.user)
    const profile_manager = useSelector(state => state.profile)
    const isAuthenticated = user_manager.isAuthenticated;
    const user = user_manager.user;
    const profile = profile_manager

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

    React.useEffect(()=> {
        authServices.profile(dispatch);
    }, [])

    
    const handleCreateView = () => {setShowList(!showList)}
    const handleShowDetail = () => {setShowDetail(true)}

    return (
        <div>
            {showDetail ? <PortfolioDetailComponent /> : null}
            <NavbarComponent />
            {showDetail ? null :
            <main className="main-content border-radius-lg">
                <TopNavbarComponent />
                <div className="container-fluid py-4">
                    <div className="row">
                        <div className="col-4">
                            <div className="card">
                                <div className="card-header">
                                    <h4>{user.username}</h4>
                                </div>
                                <div className="card-body">
                                    <ul>
                                        <li>Starting Value: {profile_manager.starting_value}</li>
                                        <li>Current Value: {profile_manager.current_value}</li>
                                        
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div className="col-8">
                            <div className="card">
                                <div className="card-header">
                                    <button onClick={handleCreateView} className="btn btn-sucess">CREATE PORTFOLIO</button>
                                </div>
                                <div className="card-body">
                                    {showList ? <PortfolioListComponent showDetail={handleShowDetail} /> : <PortfolioCreateComponent closeWindow={handleCreateView} />}
                                </div>
                            </div>
                            
                        </div>
                    </div>
                </div>
            </main>
            }

        </div>
    )
}