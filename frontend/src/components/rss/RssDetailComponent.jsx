import * as React from "react";
import { useDispatch, useSelector } from "react-redux";
import NavbarComponent from "../navbar";
import TopNavbarComponent from "../TopNavbar";



export default function RssDetailComponent(){
    const dispatch = useDispatch();
    const rss_manager = useSelector(state=>state.rss);
    const rss_detail = rss_manager.rss_detail;



    return (
        <div className="container-fluid py-4">
            <div className="row">
                <div className="col-4">
                    <div class="alert alert-primary" role="alert">
                            {rss_detail.title}
                    </div>
                </div>
            </div>
        </div>
    )
}
