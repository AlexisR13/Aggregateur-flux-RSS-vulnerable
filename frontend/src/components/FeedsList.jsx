import { useState } from "react";
import { useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";

export default function FluxList(props) {
    const [displayFavOnly, setDisplayFavOnly] = useState(false);
    const token = useSelector((state) => state.token.value);
    const navigate = useNavigate();

    // Update which flux are marked as favorite (star is full)
    function updateIsFavorite(idx) {
        // Ask user to authenticated to see its favorites
        if (!token) {
        navigate('/connexion');
        }
        else {
        const newArray = [...props.isFavorite];
        newArray[idx] = !newArray[idx];
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
                {Object.keys(props.fluxRSS).map((name, idx) => {
                    if (!displayFavOnly || props.isFavorite[idx]) {
                        return(
                        <li key={name}>
                            <button onClick={() => updateIsFavorite(idx)}>
                                {props.isFavorite[idx] ? '★' : '☆'}
                            </button>
                            <Link to={'feed/'+name} className='ml-4 text-blue-700'>
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