import axios from 'axios';
import {useEffect, useState} from 'react';
import { useParams } from 'react-router-dom';

function ArticleCard({article}) {
  return (
    <div className='m-3 p-2 border'>
      <h3 className='text-lg font-bold'>{article.title}</h3>
      <p><b>Auteur :</b> {article.author}</p>
      <p><b>Sommaire :</b> {article.summary}</p>
    </div>
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
          { fluxRSS ?
            fluxRSS.map((item) =>
              <ArticleCard article={item} key={item.title}/>
              ) :
            <p>Un problème est survenue pour récupérer le feed</p>
          }
        </div>
    </div>
  );
}

export default FeedDetailsPage;
