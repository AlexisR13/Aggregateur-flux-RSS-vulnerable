import { Link, Route, Routes } from 'react-router-dom';
import './App.css';
import FeedDetailsPage from './page/FeedDetailsPage';
import HomePage from './page/HomePage';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <Link to=''>Home</Link>
        <h1>Super App</h1>
      </header>
      <Routes>
        <Route path='/' element={<HomePage/>}/>
        <Route path='/feed/:feedName' element={<FeedDetailsPage/>}/>
      </Routes>
    </div>
  );
}

export default App;
