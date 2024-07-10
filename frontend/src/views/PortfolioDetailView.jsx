import * as React from "react";
import NavbarComponent from "../components/navbar";
import TopNavbarComponent from "../components/TopNavbar";
import { useLocation } from "react-router-dom";


export default function PortfolioDetailView(){
    const location = useLocation();
    const pathname = location.pathname;
    console.log(pathname)


    return (
        <div>
            <NavbarComponent search_type="tickers" />
            <main className="main-content border-radius-lg ">
                <TopNavbarComponent search_type="tickers" />
                <div className="container-fluid py-4">
                    <div className="row">
                        <div className="col-12">
                            <div className="card">
                                <div className="card-header">
                                    <h4>Items</h4>
                                </div>
                                <div className="card-body">
                                    <table className="table table-bordered">

                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-4">
                            <div className="card">

                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )
}