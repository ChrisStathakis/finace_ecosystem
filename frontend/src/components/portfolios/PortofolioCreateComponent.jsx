import * as React from "react";
import { useDispatch, useSelector } from "react-redux";
import portfolioServices from "../../data/services/portfolioServices";


export default function PortfolioCreateComponent(props){
    const [title, setTitle] = React.useState("");
    const [is_public, setIsPublic] = React.useState(false);

    const dispatch = useDispatch()

    const user_manager = useSelector(state => state.user);
    const user_id = user_manager.user.id;

    const handleForm = (e) => {
        e.preventDefault();
        const data = {
            title: title,
            is_public: is_public,
            user: user_id
        };

        portfolioServices.createPortfolio(data, dispatch);
        props.closeWindow();
    };

    return (
        <div>
            <h4>Create New Portfolio</h4>
            <form className="form">
                <input type="text" className="form-control" onChange={(e)=> setTitle(e.target.value)} value={title} placeholder="Title" required />


            </form>
        </div>
    )
}