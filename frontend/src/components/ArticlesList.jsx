import { Link } from 'react-router-dom';
import Loader from './Loader';

function ArticleCard({feedName, articleId, article}) {
  // article = { name: <feedname>, title: <text>, published: <date>, summary: <text> }
  // TO DO : feedname ???
  return (
    <Link to={'/article/?feed_name='+feedName+'&id='+articleId} className='mx-12 mb-4 p-3 border flex'>
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


export default function ArticlesList(props) {

  return (
    <div>
      { Object.keys(props.articles).length===0 ?
        <Loader/> :
        <div className='h-screen overflow-auto'>
          { props.articles.map((item, idx) =>
            <ArticleCard articleId={idx} article={item} key={item.title}/>
          )}
        </div>
      }
    </div>
  );
}
