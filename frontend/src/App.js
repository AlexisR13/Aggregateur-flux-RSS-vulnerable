import { Link, Route, Routes } from 'react-router-dom';
import ArticleDetailsPage from './page/ArticleDetailsPage';
import FeedDetailsPage from './page/FeedDetailsPage';
import HomePage from './page/HomePage';

function App() {

  return (
    <div>
      <header className='fixed w-full bg-slate-900 text-center text-white text-6xl flex justify-between items-center py-6'>
        <Link to='' className='text-base pl-5'>Accueil</Link>
        <h1>Super App</h1>
        <p></p>
      </header>
      <div className='pt-44 mx-32'>
        <Routes>
          <Route path='/' element={<HomePage/>}/>
          <Route path='/feed/:feedName' element={<FeedDetailsPage/>}/>
          <Route path='/article/' element={<ArticleDetailsPage/>}/>
        </Routes>
      </div>
    </div>
  );
}

export default App;
