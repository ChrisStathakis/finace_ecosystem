import * as React from "react";
import { useDispatch, useSelector } from 'react-redux';
import SearchService from "../data/services/search.service";
import tickerServices from "../data/services/ticker.services";
import rssServices from "../data/services/rss.sevices";


export default function TopNavbarComponent(props){
    const [q, setQ] = React.useState("");
    const dispatch = useDispatch();
 


    React.useEffect(()=>{
        if (props.search_type === "tickers") {
            SearchService.search_tickers(q, dispatch);
            tickerServices.fetchTickers(q, dispatch);
        }
        if (props.search_type === "rss"){
            SearchService.search_tickers(q, dispatch);
            rssServices.fetch_rss_list(q, dispatch);
        }
    }, [q]);

    return (
        <nav className="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl" id="navbarBlur" data-scroll="true">
            <div className="container-fluid py-1 px-3">
                <nav aria-label="breadcrumb">
                    <ol className="breadcrumb bg-transparent mb-0 pb-0 pt-1 px-0 me-sm-6 me-5">
                        <li className="breadcrumb-item text-sm"><a class="opacity-5 text-dark" href="javascript:;">Pages</a></li>
                        <li className="breadcrumb-item text-sm text-dark active" aria-current="page">index</li>
                    </ol>
                    <h6 className="font-weight-bolder mb-0">index</h6>
                    
                </nav>
                <div className="collapse navbar-collapse mt-sm-0 mt-2 me-md-0 me-sm-4" id="navbar">
                    <div className="ms-md-auto pe-md-3 d-flex align-items-center">
                        
                        <div className="input-group input-group-outline">
                        <label className="form-label"></label>
                        <input onChange={(e)=> setQ(e.target.value)} value={q} type="text" className="form-control" />
                        </div>
                        
                    </div>
                    <ul className="navbar-nav  justify-content-end">
                        
                   
                    <li className="nav-item d-xl-none ps-3 d-flex align-items-center">
                        <a href="javascript:;" className="nav-link text-body p-0" id="iconNavbarSidenav">
                        <div className="sidenav-toggler-inner">
                            <i className="sidenav-toggler-line"></i>
                            <i className="sidenav-toggler-line"></i>
                            <i className="sidenav-toggler-line"></i>
                        </div>
                        </a>
                    </li>
                    <li className="nav-item px-3 d-flex align-items-center">
                        <a href="javascript:;" className="nav-link text-body p-0">
                        <i className="fa fa-cog fixed-plugin-button-nav cursor-pointer"></i>
                        </a>
                    </li>
                    <li className="nav-item dropdown pe-2 d-flex align-items-center">
                        <a href="javascript:;" className="nav-link text-body p-0" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fa fa-bell cursor-pointer"></i>
                        </a>

                        <ul className="dropdown-menu  dropdown-menu-end  px-2 py-3 me-sm-n4" aria-labelledby="dropdownMenuButton">
                        <li className="mb-2">
                            <a className="dropdown-item border-radius-md" href="javascript:;">
                            <div className="d-flex py-1">
                                <div className="my-auto">
                                <img src="./assets/img/team-2.jpg" className="avatar avatar-sm  me-3 " />
                                </div>
                                <div className="d-flex flex-column justify-content-center">
                                <h6 className="text-sm font-weight-normal mb-1">
                                    <span className="font-weight-bold">New message</span> from Laur
                                </h6>
                                <p className="text-xs text-secondary mb-0">
                                    <i className="fa fa-clock me-1"></i>
                                    13 minutes ago
                                </p>
                                </div>
                            </div>
                            </a>
                        </li>
                        <li className="mb-2">
                            <a className="dropdown-item border-radius-md" href="javascript:;">
                            <div className="d-flex py-1">
                                <div className="my-auto">
                                
                                </div>
                                <div className="d-flex flex-column justify-content-center">
                                <h6 className="text-sm font-weight-normal mb-1">
                                    <span className="font-weight-bold">New album</span> by Travis Scott
                                </h6>
                                <p className="text-xs text-secondary mb-0">
                                    <i className="fa fa-clock me-1"></i>
                                    1 day
                                </p>
                                </div>
                            </div>
                            </a>
                        </li>
                        <li>
                            <a className="dropdown-item border-radius-md" href="javascript:;">
                            <div className="d-flex py-1">
                                <div className="avatar avatar-sm bg-gradient-secondary  me-3  my-auto">
                               
                                </div>
                                <div className="d-flex flex-column justify-content-center">
                                <h6 className="text-sm font-weight-normal mb-1">
                                    Payment successfully completed
                                </h6>
                                <p className="text-xs text-secondary mb-0">
                                    <i className="fa fa-clock me-1"></i>
                                    2 days
                                </p>
                                </div>
                            </div>
                            </a>
                        </li>
                        </ul>
                    </li>
                    <li className="nav-item d-flex align-items-center">
                    
                        <a href="/login" className="nav-link text-body font-weight-bold px-0"> </a>
                
                        <i className="fa fa-user me-sm-1"></i>
                        <span className="d-sm-inline d-none">Sign In</span>
                        
                        
                       
                    </li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}