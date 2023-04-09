import { useState } from 'react';
import Cookies from 'js-cookie';
import { Navigate } from 'react-router-dom';
import SignForm from '../components/SignForm';

export default function SignInPage(props) {
    // States for registration
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    // States for checking the errors
    const [error, setError] = useState(false);

    // Handling the form submission
    function handleSubmit(e) {
        e.preventDefault();
        if (username === 'admin' && password === 'admin') {
            setError(false);
            Cookies.set('username', 'admin');
            props.setAuthToken(Cookies.get('username'));
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
            title='Connexion'
            username={username}
            setUsername={setUsername}
            password={password}
            setPassword={setPassword}
            submitButtonText='Se connecter'
            handleSubmit={handleSubmit}
            error={error}
            errorMessage='Identifiants invalides !'
            alternateActionText="S'inscrire"
            alternateActionUrl='/inscription'
        />
    );
}