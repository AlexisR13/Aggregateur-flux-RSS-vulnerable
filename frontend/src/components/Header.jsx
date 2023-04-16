import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { removeToken } from '../redux/token';
import { Home, Person } from '@mui/icons-material';
import axios from 'axios';

export default function Header() {
    const dispatch = useDispatch();
    const token = useSelector((state) => state.token.value);

    function signout() {
        dispatch(removeToken());
        axios.get('/logout', { headers: { Authorization: `Bearer ${token}` }});
    }

    return (
        <header className='fixed w-full px-5 py-6 bg-slate-900 text-center text-white flex justify-between items-center'>
            <Link to=''><Home fontSize='large'/></Link>
            <h1 className='text-6xl'>FeedMeBaby</h1>
            <div>
                <Link to='profil'>
                    <Person fontSize='large'/>
                </Link><br/>
                { /* Check cookie value to see if user is authenticated or not */
                    token ?
                    <button onClick={signout}>Se déconnecter</button> :
                    <Link to='connexion'>Se connecter</Link>
                }
            </div>
        </header>
    );
}