import axios from 'axios';
import { useState } from 'react';
import Cookies from 'js-cookie';
import { Navigate } from 'react-router-dom';
import SignForm from '../components/SignForm';

export default function SignUpPage() {
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
                        console.log('VICTORY')
                        // set cookie ??
                    } else {
                        setErrorMessage(resp.message);
                    }
                })
        } else {
            setErrorMessage('Veuillez renseigner tous les champs.');
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
            errorMessage={errorMessage}
            alternateActionText='Se connecter'
            alternateActionUrl='/connexion'
            displayEmail
            email={email}
            setEmail={setEmail}
        />
    );
}