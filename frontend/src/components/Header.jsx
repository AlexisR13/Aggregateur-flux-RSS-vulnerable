import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { removeAuthCookie } from '../redux/cookies';
import { Home, Person } from '@mui/icons-material';

export default function Header() {
    const dispatch = useDispatch();
    const authCookie = useSelector((state) => state.authCookie.value);

    return (
        <header className='fixed w-full px-5 py-6 bg-slate-900 text-center text-white flex justify-between items-center'>
            <Link to=''><Home fontSize='large'/></Link>
            <h1 className='text-6xl'>FeedMeBaby</h1>
            <div>
                <Person fontSize='large'/><br/>
                { /* Check cookie value to see if user is authenticated or not */
                    authCookie ?
                    <button onClick={() => {dispatch(removeAuthCookie(undefined))}}>Se déconnecter</button> :
                    <Link to='connexion'>Se connecter</Link>
                }
            </div>
        </header>
    );
}