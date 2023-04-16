import { useState } from "react";
import { useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";

export default function FeedsList(props) {
    const [displayFavOnly, setDisplayFavOnly] = useState(false);
    const token = useSelector((state) => state.token.value);
    const navigate = useNavigate();

    // Update which flux are marked as favorite (star is full)
    function updateIsFavorite(id) {
        // Ask user to authenticated to see its favorites
        if (!token) {
            navigate('/connexion');
        }
        else {
            const newArray = [...props.isFavorite];
            newArray[id] = !newArray[id];
            props.setIsFavorite(newArray);
        }
    }

    return (
        <div>
            <button className='mb-2 px-1 text-sm border' onClick={() => setDisplayFavOnly(!displayFavOnly)}>
                {displayFavOnly ?
                'Afficher tous les flux' :
                'Afficher seulement les flux favoris'
                }
            </button>
            <ul className='list-inside'>
                {Object.entries(props.feeds).map(([name, feed]) => {
                    if (!displayFavOnly || props.isFavorite[feed.id]) {
                        return(
                        <li key={feed.id}>
                            <button onClick={() => updateIsFavorite(feed.id)}>
                                {props.isFavorite[feed.id] ? '★' : '☆'}
                            </button>
                            <Link to={'feed/'+feed.id} className='ml-4 text-blue-700'>
                                {name}
                            </Link>
                        </li>
                    )} else {
                        return(<></>)
                    }
                })}
            </ul>
        </div>
    );
}