import * as React from "react";
import { useDispatch, useSelector } from "react-redux";

import NavbarComponent from "../components/navbar";
import TopNavbarComponent from "../components/TopNavbar";
import rssSevices from "../data/services/rss.sevices";
import RssListComponent from "../components/rss/RssListComponent";
import RssDetailComponent from "../components/rss/RssDetailComponent";




export default function RssViewList() {
    const [showList, setShowList] = React.useState(true);


    return (
        <div>
        
            <NavbarComponent search_type="tickers" />
            <main className="main-content border-radius-lg ">
                <TopNavbarComponent search_type="rss" />
                {showList ? <RssListComponent handleButton={() => setShowList(false)} /> : <RssDetailComponent handleButton={() => setShowList(true)} />}
            </main>
        </div>
    )
}