import { Route, Routes } from 'react-router-dom';
import SignInPage from './page/SignInPage';
import SignUpPage from './page/SignUpPage';
import HomePage from './page/HomePage';
import Header from './components/Header';

function App() {
  return (
    <div>
      <Header/>
      <div className='pt-44'>
        <Routes>
          <Route path='/' element={<HomePage/>}/>
          <Route path='/connexion/' element={<SignInPage/>}/>
          <Route path='/inscription/' element={<SignUpPage/>}/>
        </Routes>
      </div>
    </div>
  );
}

export default App;
