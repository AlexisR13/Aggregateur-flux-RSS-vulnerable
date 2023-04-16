import axios from 'axios';
import { useEffect, useState } from 'react';
import Loader from '../Loader';
import ArticlesList from '../ArticlesList';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

export default function FavoriteArticlesListPannel() {
  const [articles, setArticles] = useState([])
  const token = useSelector((state) => state.token.value);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate('/connexion');
    }
    else {
      axios.get('/articles?filter=favs',
      { headers: { Authorization: `Bearer ${token}` }}
    )
      .then((response) => {
        setArticles(response.data);
    })
    }
  }, [navigate, token])

  return (
    <div>
      { Object.keys(articles).length===0 ?
        <Loader/> :
        <ArticlesList articles={articles}/>
      }
    </div>
  );
}
