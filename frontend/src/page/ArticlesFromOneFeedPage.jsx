import axios from 'axios';
import { useEffect, useState } from 'react';
import Loader from '../components/Loader';
import ArticlesList from '../components/ArticlesList';
import { useParams } from 'react-router-dom';

export default function ArticlesFromOneFeedPage() {
    const { feedId } = useParams();

    const [articles, setArticles] = useState([])
    useEffect(() => {
    axios.get('/articles?feed=' + feedId)
        .then((response) => {
        setArticles(response.data);
    })
    }, [feedId])

  return (
    <div>
      { Object.keys(articles).length===0 ?
        <Loader/> :
        <ArticlesList articles={articles}/>
      }
    </div>
  );
}
