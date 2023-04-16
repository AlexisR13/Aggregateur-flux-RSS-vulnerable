import axios from 'axios';
import { useEffect, useState } from 'react';
import Loader from '../Loader';
import ArticlesList from '../ArticlesList';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

export default function FavoriteArticlesListPannel() {
  const [articles, setArticles] = useState([])
  const [isLoading, setIsLoading] = useState(true)
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
        setIsLoading(false);
    })
    }
  }, [navigate, token])

  return (
    <div>
      { isLoading ?
         <Loader/> :
        <>
        { Object.keys(articles).length===0 ?
          <p className='ml-12 mt-10'>Ajoutez des feeds aux favoris pour les retrouver ici !</p> :
          <ArticlesList articles={articles}/>
        }
        </>
      }
    </div>
  );
}
