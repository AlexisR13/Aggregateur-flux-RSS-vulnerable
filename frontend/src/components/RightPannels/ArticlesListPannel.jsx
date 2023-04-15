import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Loader from '../Loader';

function ArticleCard({feedName, articleId, article}) {
  // article = { name: <feedname>, title: <text>, published: <date>, summary: <text> }
  // TO DO : feedname ???
  return (
    <Link to={'/article/?feed_name='+feedName+'&id='+articleId} className='mr-12 mb-4 p-3 border flex'>
      <div className='w-1/4'>
        <h3>{article.name}</h3>
      </div>
      <div className='w-3/4'>
        <h3 className='text-lg font-bold'>{article.title}</h3>
        <p>{article.summary}</p>
      </div>
    </Link>
  )
}


export default function ArticlesListPannel(props) {
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
        <div className='h-screen overflow-auto'>
          { articles.map((item, idx) =>
            <ArticleCard articleId={idx} article={item} key={item.title}/>
          )}
        </div>
      }
    </div>
  );
}
