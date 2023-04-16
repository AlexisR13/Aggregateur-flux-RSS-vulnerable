import { useState } from 'react';
import LeftPannel from '../components/Pannels/LeftPannel';
import FeedsListPannel from '../components/Pannels/FeedsListPannel';
import ArticlesListPannel from '../components/Pannels/ArticlesListPannel';
import FavoriteArticlesListPannel from '../components/Pannels/FavoriteArticlesListPannel';
import { useSelector } from 'react-redux';

function HomePage() {
  const token = useSelector((state) => state.token.value);
  const [pannelSelected, setPannelSelected] = useState(token ? 'home' : 'all')

  return (
    <div className='flex'>
      <LeftPannel pannelSelected={pannelSelected} setPannelSelected={setPannelSelected}/>
      
      {
        pannelSelected==='home' && (<FavoriteArticlesListPannel/>)
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
