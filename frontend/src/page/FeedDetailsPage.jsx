import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

function ArticleCard({feedName, articleId, article}) {
  return (
    <Link to={'/article/?feed_name='+feedName+'&id='+articleId} className='m-2'>
      <div className='p-3 border'>
        <h3 className='text-lg font-bold'>{article.title}</h3>
        <p><b>Auteur :</b> {article.author}</p>
        <p><b>Sommaire :</b> {article.summary}</p>
      </div>
    </Link>
  )
}


function FeedDetailsPage() {
  const { feedName } = useParams();

  const [fluxRSS, setFluxRSS] = useState([])
  useEffect(() => {
    axios.get('http://localhost:5000/'+feedName)
      .then((response) => {
        setFluxRSS(response.data);
    })
  }, [feedName])

  return (
    <div>
        <h1 className='text-3xl mb-5'>Bienvenue sur le feed : {feedName}</h1>
        <div>
          { fluxRSS.length>0 ?
            fluxRSS.map((item, idx) =>
              <ArticleCard feedName={feedName} articleId={idx} article={item} key={item.title}/>
              ) :
            <p>Un problème est survenue pour récupérer le feed. <br/>
            Veuillez vérifier votre connexion internet, ou réessayer ultérieurement.</p>
          }
        </div>
    </div>
  );
}

export default FeedDetailsPage;
