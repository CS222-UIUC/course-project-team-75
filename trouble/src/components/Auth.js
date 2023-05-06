import "../styles/Auth.css";
import {auth, provider} from '../firebase_config.js';
// //provider is the google account provided to authenticate usere
import {signInWithPopup} from "firebase/auth"; //used when u wanna sign in with any kind of pop up like google or GitHub

import Cookies from 'universal-cookie';
const cookies = new Cookies();

export const Auth = (props) => {

    const {setIsAuth} = props;

    //asynchronous functionality -> async()
    const signInWithGoogle = async() =>{
        try{
        const result = await signInWithPopup(auth, provider);
        console.log(result);
        cookies.set("auth-token",result.user.refreshToken);
        setIsAuth(true);

        } catch(err){
            console.error(err);
        }

    };


    return (<div className="auth">
        <h1 className="Head">Welcome to</h1>

       
        <div className="header">
      <div>Trou<span>ble</span></div>
      <img
        className="logo"
        src={require('../output_onlinepngtools.png')}
        alt="straight man walking susical"
      />
     </div>
       
    
      
    
        
        <div className="sign">
        <p>Sign in With Google To Continue</p>
        </div>
        <button className = "sign-in" onClick={signInWithGoogle}>Sign In With Google</button>


    </div>
    );

};

export default Auth;