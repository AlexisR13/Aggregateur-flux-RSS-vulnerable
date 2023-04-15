import axios from 'axios';
import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

function ArticleDetailsPage() {
  const [searchParams] = useSearchParams();
  const feedName = searchParams.get('feed_name');
  const articleId = searchParams.get('id');

  const [article, setArticle] = useState([])
  useEffect(() => {
    axios.get(feedName + '/' + articleId)
      .then((response) => {
        setArticle(response.data);
    })
  }, [feedName, articleId])

  return (
    <div>
        <h1 className='text-3xl mb-5'>{article.title}</h1>
        <p><b>Auteur :</b> {article.author}</p>
        <p><b>Sommaire :</b> {article.summary}</p>
        <p><b>Lien :</b> <a href={article.link} className='text-blue-600'>{article.link}</a></p>
        { article.content?.value &&
          <p><b>Contenu :</b>{article.content.value}</p>
        }
    </div>
  );
}

export default ArticleDetailsPage;
