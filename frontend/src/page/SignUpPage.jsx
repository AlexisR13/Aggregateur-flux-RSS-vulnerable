import { useState } from 'react';
import Cookies from 'js-cookie';
import { Navigate } from 'react-router-dom';
import SignForm from '../components/SignForm';

export default function SignUpPage() {
    // States for registration
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    // States for checking the errors
    const [error, setError] = useState(false);

    // Handling the form submission
    function handleSubmit(e) {
        e.preventDefault();
        if (1==2) {
            // Do stuff here
            setError(false);
        } else {
            setError(true);
        }
    };

    // If user is already connected, just redirect them
    if (Cookies.get('username')) {
        return <Navigate replace to='/'/>
    }

    return (
        <SignForm 
            title='Inscription'
            username={username}
            setUsername={setUsername}
            password={password}
            setPassword={setPassword}
            submitButtonText="S'inscrire"
            handleSubmit={handleSubmit}
            error={error}
            errorMessage='Une erreur est survenue. Veuillez réessayer ultérieurement.'
            alternateActionText='Se connecter'
            alternateActionUrl='/connexion'
        />
    );
}