import { Link, Route, Routes } from 'react-router-dom';
import FeedDetailsPage from './page/FeedDetailsPage';
import HomePage from './page/HomePage';

function App() {

  return (
    <div>
      <header className='bg-slate-900 text-center text-white text-6xl flex justify-center items-center py-6 mb-20'>
        <Link to='' className='text-base'>Home</Link>
        <h1>Super App</h1>
      </header>
      <div className='mx-32'>
        <Routes>
          <Route path='/' element={<HomePage/>}/>
          <Route path='/feed/:feedName' element={<FeedDetailsPage/>}/>
        </Routes>
      </div>
    </div>
  );
}

export default App;
