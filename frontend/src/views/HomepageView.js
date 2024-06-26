import * as React from 'react';
import NavbarComponent from '../components/navbar';
import TopNavbarComponent from '../components/TopNavbar';







export default function  HomepageView() {
    

    return (
        <div>
            <NavbarComponent />
            <main className="main-content border-radius-lg ">
                <TopNavbarComponent />
                <div className="container-fluid py-4">

                </div>
            </main>
        </div>
    )
}