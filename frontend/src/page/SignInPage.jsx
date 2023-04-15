import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import SignForm from '../components/SignForm';
import { useDispatch, useSelector } from 'react-redux';
import { setAuthCookie } from '../redux/cookies';
import axios from 'axios';

export default function SignInPage() {
    const dispatch = useDispatch();

    // States for registration
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    // States for checking the errors
    const [errorMessage, setErrorMessage] = useState('');

    // Handling the form submission
    function handleSubmit(e) {
        e.preventDefault();
        if (username && password) {
            axios.post('/login', {
                username,
                password
            })
                .then((response) => {
                    const resp = response.data;
                    if (resp.success) {
                        console.log('VICTORY')
                        // TO DO - backend set cookie instead of frontend
                        dispatch(setAuthCookie('admin'));
                    } else {
                        setErrorMessage('Identifiants invalides !');
                    }
                })
        } else {
            setErrorMessage('Veuillez remplir tous les champs.');
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
            errorMessage={errorMessage}
            alternateActionText="S'inscrire"
            alternateActionUrl='/inscription'
        />
    );
}