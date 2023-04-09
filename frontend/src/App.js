import { Link, Route, Routes } from 'react-router-dom';
import { useState } from 'react';
import Cookies from 'js-cookie';
import SignInPage from './page/SignInPage';
import SignUpPage from './page/SignUpPage';
import ArticleDetailsPage from './page/ArticleDetailsPage';
import FeedDetailsPage from './page/FeedDetailsPage';
import HomePage from './page/HomePage';

function App() {
  const [authToken, setAuthToken] = useState(Cookies.get('username'))  
  console.log(authToken)

  return (
    <div>
      <header className='fixed w-full px-5 py-6 bg-slate-900 text-center text-white flex justify-between items-center'>
        <Link to=''>Accueil</Link>
        <h1 className='text-6xl'>Super App</h1>
        { /* Check cookie value to see if user is authenticated or not */
          authToken ?
          <button onClick={() => {Cookies.remove('username'); setAuthToken(undefined)}}>Se déconnecter</button> :
          <Link to='connexion'>Se connecter</Link>
        }
      </header>
      <div className='pt-44 mx-32'>
        <Routes>
          <Route path='/' element={<HomePage/>}/>
          <Route path='/connexion/' element={<SignInPage setAuthToken={setAuthToken}/>}/>
          <Route path='/inscription/' element={<SignUpPage/>}/>
          <Route path='/feed/:feedName' element={<FeedDetailsPage/>}/>
          <Route path='/article/' element={<ArticleDetailsPage/>}/>
        </Routes>
      </div>
    </div>
  );
}

export default App;
