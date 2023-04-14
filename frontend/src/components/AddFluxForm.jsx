import { useState } from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

export default function AddFluxForm(props) {
    const [fluxName, setFluxName] = useState('');
    const [fluxURL, setFluxURL] = useState('');
    const [error, setError] = useState(false);
    const authCookie = useSelector((state) => state.authCookie.value);
    const navigate = useNavigate();

    function handleSubmit(e) {
        e.preventDefault();
        if (!authCookie) {
            navigate('/connexion');
        } else {
            setError(true);
        }
    }

    // Showing error message if error is true
    function ErrorMessage() {
        return (
            <div className="bg-red-400 w-max px-3 py-1 mb-4" style={{display: error ? '' : 'none'}}>
                <p>Ajout impossible</p>
            </div>
        );
    };

    return (
        <div className='mt-14 border p-4'>
        <h2 className='text-2xl mb-4'>Ajouter un flux supplémentaire :</h2>
        <ErrorMessage/>
        <form>
            <label>Nom du flux :</label>
            <input type='text'
                value={fluxName}
                onChange={(e) => setFluxName(e.target.value)}
                className='mx-6 p-1 border'/>
            <label>URL du flux :</label>
            <input type='text' 
                value={fluxURL} 
                onChange={(e) => setFluxURL(e.target.value)}
                placeholder='https://example.com/feed' 
                className='ml-6 p-1 border'/>
            <button type='submit' onClick={handleSubmit} className='ml-4 p-1 bg-gray-400  rounded'>Envoyer</button>
        </form>
      </div>
    );
}