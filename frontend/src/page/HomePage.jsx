import { useState } from 'react';
import LeftPannel from '../components/LeftPannel';
import FeedsListPannel from '../components/RightPannels/FeedsListPannel';
import ArticlesListPannel from '../components/RightPannels/ArticlesListPannel';

function HomePage() {
  const [pannelSelected, setPannelSelected] = useState('home')

  return (
    <div className='flex'>
      <LeftPannel pannelSelected={pannelSelected} setPannelSelected={setPannelSelected}/>
      
      {
        pannelSelected==='home' && (<></>)
      }
      {
        pannelSelected==='all' && (<ArticlesListPannel/>)
      }
      {
        pannelSelected==='feeds' && (<FeedsListPannel/>)
      }
    </div>
  );
}

export default HomePage;
