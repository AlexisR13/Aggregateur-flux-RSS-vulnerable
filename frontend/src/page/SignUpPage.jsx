import axios from 'axios';
import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import SignForm from '../components/SignForm';
import { useDispatch, useSelector } from 'react-redux';
import { setToken } from '../redux/token';

export default function SignUpPage() {
    const dispatch = useDispatch();

    // States for registration
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    // States for checking the errors
    const [errorMessage, setErrorMessage] = useState('');

    // Handling the form submission
    function handleSubmit(e) {
        e.preventDefault();
        if (username && email && password) {
            axios.post('/signup', {
                username,
                email,
                password
            })
                .then((response) => {
                    const resp = response.data;
                    if (resp.success) {
                        dispatch(setToken(resp.access_token));
                    } else {
                        setErrorMessage(resp.message);
                    }
                })
        } else {
            setErrorMessage('Veuillez renseigner tous les champs.');
        }
    };

    // If user is already connected, just redirect them
    if (useSelector((state) => state.token.value)) {
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
            errorMessage={errorMessage}
            alternateActionText='Se connecter'
            alternateActionUrl='/connexion'
            displayEmail
            email={email}
            setEmail={setEmail}
        />
    );
}