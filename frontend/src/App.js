import logo from './logo.svg';
import {
  createBrowserRouter,
  RouterProvider,
  createRoutesFromElements, Route
} from "react-router-dom";
import './App.css';
import HomepageView from './views/HomepageView';
import  TickerView from "./views/TickersView.jsx"
import RssViewList from './views/RssViewList.jsx';
import UserView from './views/UserView.jsx';
import LoginView from './views/LoginView.jsx';
import LogoutComponent from './components/LogoutComponent.jsx';
import PortfolioDetailView from './views/PortfolioDetailView.jsx';
import ErrorPage from './views/ErrorPage.jsx';




const router = createBrowserRouter([
  {
    path: "/",
    element: <HomepageView />,
    errorElement: <ErrorPage />
  },
  {
    path: "/tickers",
    element: <TickerView />
  },
  {
    path:"/rss",
    element: <RssViewList />
  },
  {
    path:"/user",
    element: <UserView />
  },
  {
    path: "/login",
    element: <LoginView />
  },
  {
    path:"/logout",
    element: <LogoutComponent />
  },
  {
    path:"/port",
    element: <PortfolioDetailView />,
    errorElement: <ErrorPage />
  }
])


function App() {
  return (
    <div className="App">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
