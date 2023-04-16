import axios from 'axios';
import {useEffect, useState} from 'react';
import FeedsList from '../FeedsList';
import Loader from '../Loader';
import AddFeedForm from '../AddFeedForm';

export default function FeedsListPannel() {
  const [feeds, setFeeds] = useState({});
  const [isFavorite, setIsFavorite] = useState([]);

  // Get flux RSS list from backend
  useEffect(() => {
    axios.get('/')
    .then((response) => {
      setFeeds(response.data);
      setIsFavorite(Object.keys(response.data).map(() => false));
    })
  }, [])

  return (
    <div className='ml-12'>
        { Object.keys(feeds).length===0 ?
        // Loading...
        <Loader/> :
        // Flux list
        <FeedsList feeds={feeds} isFavorite={isFavorite} setIsFavorite={setIsFavorite}/>
        }
        <AddFeedForm/>
    </div>
  );
}
