import axios from "axios";
import { useState } from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

export default function AddFeedForm() {
    const [name, setName] = useState('');
    const [url, setUrl] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const token = useSelector((state) => state.token.value);
    const navigate = useNavigate();

    function handleSubmit(e) {
        e.preventDefault();
        if (!token) {
            navigate('/connexion');
        } else {
            if (name && url) {
                axios.post('/manage_feed', 
                        { name, url},
                        { headers: { Authorization: `Bearer ${token}` }}
                    )
                    .then((response) => {
                        const resp = response.data;
                        if (resp.success) {
                            setErrorMessage('');
                            setSuccessMessage('Flux ajouté !');
                        } else {
                            setSuccessMessage('');
                            setErrorMessage(resp.message);
                        }
                    })
            } else {
                setErrorMessage('Veuillez renseigner tous les champs.');
            }
        }
    }

    // Showing error or success message
    function Message() {
        return (
            <div className={"w-max px-3 py-1 mb-4 " + (errorMessage?'bg-red-400':'bg-green-400')} 
                style={{display: (errorMessage || successMessage) ? '' : 'none'}}>
                <p>{errorMessage || successMessage}</p>
            </div>
        );
    };

    return (
        <div className='mt-14 border p-4'>
        <h2 className='text-2xl mb-4'>Ajouter un flux supplémentaire :</h2>
        <Message/>
        <form>
            <label>Nom du flux :</label>
            <input type='text'
                value={name}
                onChange={(e) => setName(e.target.value)}
                className='mx-6 p-1 border'/>
            <label>URL du flux :</label>
            <input type='text' 
                value={url} 
                onChange={(e) => setUrl(e.target.value)}
                placeholder='https://example.com/feed' 
                className='ml-6 p-1 border'/>
            <button type='submit' onClick={handleSubmit} className='ml-4 p-1 bg-gray-400  rounded'>Envoyer</button>
        </form>
      </div>
    );
}