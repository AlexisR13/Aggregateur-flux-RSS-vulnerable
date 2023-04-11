import { Link, Route, Routes } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { removeAuthCookie } from './redux/cookies';
import SignInPage from './page/SignInPage';
import SignUpPage from './page/SignUpPage';
import ArticleDetailsPage from './page/ArticleDetailsPage';
import FeedDetailsPage from './page/FeedDetailsPage';
import HomePage from './page/HomePage';

function App() {
  const dispatch = useDispatch();
  const authCookie = useSelector((state) => state.authCookie.value);

  return (
    <div>
      <header className='fixed w-full px-5 py-6 bg-slate-900 text-center text-white flex justify-between items-center'>
        <Link to=''>Accueil</Link>
        <h1 className='text-6xl'>Super App</h1>
        { /* Check cookie value to see if user is authenticated or not */
          authCookie ?
          <button onClick={() => {dispatch(removeAuthCookie(undefined))}}>Se déconnecter</button> :
          <Link to='connexion'>Se connecter</Link>
        }
      </header>
      <div className='pt-44 mx-32'>
        <Routes>
          <Route path='/' element={<HomePage/>}/>
          <Route path='/connexion/' element={<SignInPage/>}/>
          <Route path='/inscription/' element={<SignUpPage/>}/>
          <Route path='/feed/:feedName' element={<FeedDetailsPage/>}/>
          <Route path='/article/' element={<ArticleDetailsPage/>}/>
        </Routes>
      </div>
    </div>
  );
}

export default App;
