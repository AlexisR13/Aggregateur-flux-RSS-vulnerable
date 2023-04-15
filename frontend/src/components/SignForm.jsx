import { Link } from "react-router-dom";

/*
Props : 
- title
- username
- setUsername
- password
- setPassword
- submitButtonText
- handleSubmit
- errorMessage
- alternateActionText
- alternateActionUrl
- displayEmail  (optional)
- email         (optional)
- setEmail      (optional)
*/
export default function SignForm(props) {
    // Handling the username change
    function handleUsername(e) {
        props.setUsername(e.target.value);
    };

    // Handling the password change
    function handlePassword(e) {
        props.setPassword(e.target.value);
    };

    // Handling the password change
    function handleEmail(e) {
        props.setEmail(e.target.value);
    };

    // Showing error message if error is true
    function ErrorMessage() {
        return (
            <div className="bg-red-400 px-3 py-1 mb-4" style={{display: props.errorMessage==='' ? 'none' : ''}}>
                <h1>{props.errorMessage}</h1>
            </div>
        );
    };

    return (
        <div className="mt-10 p-10 w-min m-auto bg-gray-100 border rounded-lg flex flex-col items-center">
            <div>
                <h1 className='text-2xl mb-4'>{props.title}</h1>
            </div>

            {/* Calling to the methods */}
            <div className="text-center">
                <ErrorMessage/>
            </div>

            <form>
                {/* Labels and inputs for form data */}
                <div className='grid grid-cols-[40%_50%] gap-4 mt-4'>
                    <label>Nom d'utilisateur</label>
                    <input onChange={handleUsername} value={props.username} type="text" />

                    {props.displayEmail ?
                        <>
                            <label>Adresse email</label>
                            <input onChange={handleEmail} value={props.email} type="text" />
                        </> :
                        <></>
                    }
                    
                    <label>Mot de passe</label>
                    <input onChange={handlePassword} value={props.password} type="password" />
                </div>

                <div className="mt-12 text-center">
                    <button onClick={props.handleSubmit} 
                        className="px-4 py-2 border bg-gray-300" 
                        type="submit">
                        {props.submitButtonText}
                    </button><br/>
                    <Link to={props.alternateActionUrl} className="text-xs text-blue-900 underline">
                        {props.alternateActionText}
                    </Link>
                </div>
            </form>
        </div>
    );
}