import axios from 'axios';
import {useEffect, useState} from 'react';
import FeedsList from '../FeedsList';
import Loader from '../Loader';
import AddFeedForm from '../AddFeedForm';
import { useSelector } from 'react-redux';

export default function FeedsListPannel() {
  const [feeds, setFeeds] = useState({});
  const [isFavorite, setIsFavorite] = useState([]);
  const token = useSelector((state) => state.token.value);

  // Get flux RSS list from backend
  useEffect(() => {
    axios.get('/',
      { headers: token ? { Authorization: `Bearer ${token}` } : undefined})
    .then((response) => {
      setFeeds(response.data);
      const array = Object.keys(response.data).map(() => false);
      Object.values(response.data).map((feed) => array[feed.id]=feed.isFavorite)
      setIsFavorite(array);
    })
  }, [token])

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
