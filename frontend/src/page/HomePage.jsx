import { useState } from 'react';
import LeftPannel from '../components/Pannels/LeftPannel';
import FeedsListPannel from '../components/Pannels/FeedsListPannel';
import ArticlesListPannel from '../components/Pannels/ArticlesListPannel';

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
