import { Link } from 'react-router-dom';
import Loader from './Loader';

function ArticleCard({article}) {
  // article = { name: <feedname>, title: <text>, published_parsed: [<date>], summary: <text>, link: <url> }
  const date_array = article.published_parsed;
  const date_str = date_array[2].toString() + '/' + date_array[1].toString() + '/' + date_array[0].toString()

  return (
    <Link to={article.link}
      target="_blank" rel="noopener noreferrer"
      className='mx-12 mb-4 p-3 border flex'>
      <div className='w-1/4 flex flex-col justify-between'>
        <h3>{article.name}</h3>
        <p className='text-xs text-gray-600'>{date_str}</p>
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
