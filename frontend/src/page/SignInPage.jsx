import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import SignForm from '../components/SignForm';
import { useDispatch, useSelector } from 'react-redux';
import { setAuthCookie } from '../redux/cookies';

export default function SignInPage() {
    const dispatch = useDispatch();

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
            // TO DO - backend set cookie instead of frontend
            dispatch(setAuthCookie('admin'));
        } else {
            setError(true);
        }
    };

    // If user is already connected, just redirect them
    if (useSelector((state) => state.authCookie.value)) {
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