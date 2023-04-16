import axios from "axios";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";
import Loader from '../components/Loader';

function Form(props) {    
    return(
        <form className='my-10'>
            <p className="text-lg font-bold">{props.title}</p><br/>
            <div className="grid grid-cols-[max-content_300px]">
                <label>{props.fieldname}</label>
                <input type='text'
                    placeholder={props.placeholder}
                    value={props.value}
                    onChange={(e) => props.setValue(e.target.value)}
                    className='mx-6 p-1 border'/>
                <label>Mot de passe</label>
                <input type='password'
                    value={props.password}
                    onChange={(e) => props.setPassword(e.target.value)}
                    className='mx-6 p-1 border'/>
            </div>
            <button type='submit' onClick={props.handleSubmit} className='p-1 px-5 bg-gray-400 rounded mt-4 ml-40'>
                Modifier
            </button>
        </form>
    )
}

export default function ProfilePage() {
    const token = useSelector((state) => state.token.value);
    const [user, setUser] = useState({});
    const [password, setPassword] = useState('');
    const [newEmail, setNewEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    useEffect(() => {
        axios.get('/profile', {
            headers: { Authorization: `Bearer ${token}` }
        })
            .then((response) => {
                setUser(response.data);
            });
    }, [token])

    function handleSubmitEmail(e) {
        e.preventDefault();
        axios.post('/email',
            { newEmail, password },
            { headers: { Authorization: `Bearer ${token}` }}
            )
            .then((response) => {
                const resp = response.data;
                if (resp.success) {
                    setErrorMessage('');
                    setSuccessMessage('Email modifié !')
                } else {
                    setSuccessMessage('');
                    setErrorMessage(resp.message);
                }
            })
    }
    function handleSubmitPassword(e) {
        e.preventDefault();
        axios.post('/password',
            { newPassword, password },
            { headers: { Authorization: `Bearer ${token}` }}
            )
            .then((response) => {
                const resp = response.data;
                if (resp.success) {
                    setErrorMessage('');
                    setSuccessMessage('Mot de passe modifié !')
                } else {
                    setSuccessMessage('');
                    setErrorMessage(resp.message);
                }
            })
    }

    function ErrorMessage() {
        return (
            <div className={"w-max px-3 py-1 mb-4 " + (errorMessage?'bg-red-400':'bg-green-400')} 
                style={{display: (errorMessage || successMessage) ? '' : 'none'}}>
                <p>{errorMessage || successMessage}</p>
            </div>
        );
    };

    // If user is already connected, just redirect them
    if (!token) {
        return <Navigate replace to='/connexion'/>
    }
    console.log(user)

    return (
        <div>
            { Object.keys(user).length===0 ?
                <Loader/> :
                <div  className='ml-16'>
                    <div className='mb-20'>
                        <h1 className='text-5xl mb-4'>{user.login}</h1>
                        <p><b>Email :</b> {user.email}</p>
                        <p><b>Date de création :</b> {user.created_at}</p>
                    </div>
                    <div>
                        <ErrorMessage/>
                        <Form title="Changer l'email"
                            fieldname='Nouvel email'
                            placeholder={user.email}
                            value={newEmail}
                            setValue={setNewEmail}
                            handleSubmit={handleSubmitEmail}
                            password={password}
                            setPassword={setPassword}
                        />
                        <Form title="Changer le mot de passe"
                            fieldname='Nouveau mot de passe'
                            value={newPassword}
                            setValue={setNewPassword}
                            handleSubmit={handleSubmitPassword}
                            password={password}
                            setPassword={setPassword}
                        />
                    </div>
                </div>
            }
        </div>
    );
}