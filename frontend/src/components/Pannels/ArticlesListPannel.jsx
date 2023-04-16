import axios from 'axios';
import { useEffect, useState } from 'react';
import Loader from '../Loader';
import ArticlesList from '../ArticlesList';

export default function ArticlesListPannel() {
  const [articles, setArticles] = useState([])
  useEffect(() => {
    axios.get('/articles')
      .then((response) => {
        setArticles(response.data);
    })
  }, [])

  return (
    <div>
      { Object.keys(articles).length===0 ?
        <Loader/> :
        <ArticlesList articles={articles}/>
      }
    </div>
  );
}
