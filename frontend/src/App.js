import { Route, Routes } from 'react-router-dom';
import SignInPage from './page/SignInPage';
import SignUpPage from './page/SignUpPage';
import HomePage from './page/HomePage';
import Header from './components/Header';
import ProfilePage from './page/ProfilePage';
import ArticlesFromOneFeedPage from './page/ArticlesFromOneFeedPage';

function App() {
  return (
    <div>
      <Header/>
      <div className='pt-44'>
        <Routes>
          <Route path='/' element={<HomePage/>}/>
          <Route path='/connexion/' element={<SignInPage/>}/>
          <Route path='/inscription/' element={<SignUpPage/>}/>
          <Route path='/profil' element={<ProfilePage/>}/>
          <Route path='/feed/:feedId' element={<ArticlesFromOneFeedPage/>}/>
        </Routes>
      </div>
    </div>
  );
}

export default App;
