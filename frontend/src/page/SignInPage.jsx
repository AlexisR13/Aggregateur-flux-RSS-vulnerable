import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import SignForm from '../components/SignForm';
import { useDispatch, useSelector } from 'react-redux';
import { setToken } from '../redux/token';
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
                        dispatch(setToken(resp.access_token));
                    } else {
                        setErrorMessage('Identifiants invalides !');
                    }
                })
        } else {
            setErrorMessage('Veuillez remplir tous les champs.');
        }
    };

    // If user is already connected, just redirect them
    if (useSelector((state) => state.token.value)) {
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