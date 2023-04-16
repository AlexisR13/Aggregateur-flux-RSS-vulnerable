import axios from 'axios';
import { useEffect, useState } from 'react';
import Loader from '../Loader';
import ArticlesList from '../ArticlesList';
import { useSelector } from 'react-redux';

export default function ArticlesListPannel() {
  const [articles, setArticles] = useState([])
  const token = useSelector((state) => state.token.value);

  useEffect(() => {
    axios.get('/articles',
        { headers: token ? { Authorization: `Bearer ${token}` } : undefined}
      )
      .then((response) => {
        setArticles(response.data);
    })
  }, [token])

  return (
    <div>
      { Object.keys(articles).length===0 ?
        <Loader/> :
        <ArticlesList articles={articles}/>
      }
    </div>
  );
}
