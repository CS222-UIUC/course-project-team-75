//import logo from './logo.svg';
import './App.css';
import React, { useState, useRef } from "react";
import {Auth} from "./components/Auth";
import {Chat} from "./components/Chat";
import {signOut} from "firebase/auth";
import {auth} from "./firebase_config";

import Cookies from 'universal-cookie';
const cookies = new Cookies();


function App() {

  const [isAuth, setIsAuth] = useState(cookies.get("auth-token"));
  const [room, setRoom] = useState(null);

  const roomInputRef = useRef(null);


  const signUserOut = async () => {

    await signOut(auth);
    cookies.remove("auth-token");
    setIsAuth(false);
    setRoom(null);

  };

  if(!isAuth){

  

  return (
    <div>
      <Auth setIsAuth={setIsAuth}/>
    </div>
  );

  }

  //want to ask room name they want to join
  //if room us null, we want to display the chat
  return (
  
  
  <div>

    
        <div className="header">
      <div>Trou<span>ble</span></div>
      <img
        className="logo"
        src={require('./output_onlinepngtools.png')}
        alt="gay man walking susical"
      />
    </div>
    
   


    <div class="container">

      <div class="side">
        <div class="menu">
          <ul>
            <li>Matches</li>
            <li class="active">Messages</li>
          </ul>
        </div>
        <div class="messages">
          <div class="avatar">
            <img
              src="https://static1.cbrimages.com/wordpress/wp-content/uploads/2021/07/roz-monsters-inc-monsters-at-work.jpg"
            />
          </div>



          <div class="message">
            <div class="user">Roz</div>
            <div class="text">Looking for trouble 😘</div>
          </div>
        </div>
        <div class="messages">
          <div class="avatar">
            <img
              src="data:image/jpeg;base64,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"
              alt=""
            />
          </div>

          <div class="message">
            <div class="user">Madison Beer</div>
            <div class="text">
              This user has blocked you and you can no longer send messages
            </div>
          </div>
        </div>
        <div class="messages">
          <div class="avatar">
            <img
              src="https://randomuser.me/api/portraits/women/40.jpg"
              alt=""
            />
          </div>



          <div class="message">
            <div class="user">Caroline</div>
            <div class="text">
              This user has blocked you and you can no longer send messages
            </div>
          </div>
        </div>
        <div class="messages">
          <div class="avatar">
            <img
              src="https://randomuser.me/api/portraits/women/41.jpg"
              alt=""
            />
          </div>
          <div class="message">
            <div class="user">Karen</div>
            <div class="text">
              This user has blocked you and you can no longer send messages
            </div>
          </div>
        </div>
        <div class="messages">
          <div class="avatar">
            <img
              src="https://randomuser.me/api/portraits/women/42.jpg"
              alt=""
            />
          </div>
          <div class="message">
            <div class="user">Amy</div>
            <div class="text">
              This user has blocked you and you can no longer send messages
            </div>
          </div>
        </div>
      </div>
      <div class="content">
        
      </div>
      
    </div>







    {room ? <Chat room = {room}/> :
    
    <div className='room'>
      
      <label>Enter Room Name:</label>
      <input ref = {roomInputRef}/>
      <button onClick={() => setRoom(roomInputRef.current.value)}>Enter Chat</button>

    </div>
    
    
    }
  
    

  

			
			
    
    


    <div className = "sign-out">
      <button onClick={signUserOut}>Sign Out</button>
    </div>

  </div>

  
  
  );

}

export default App;









<div class="message">




<div class="user">Roz</div>
<div class="text">Looking for trouble 😘</div>
</div>
</div>
<div class="messages">
<div class="avatar">
<img
  src="data:image/jpeg;base64,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"
  alt=""
/>
</div>
</div>
</div>
</div>
</div>







<div class="container">
    
<div class="side">
  <div class="menu">
  <span class="active">Messages</span>
    <ul>
      <div class="divyam">
{Array.from(new Set(usersList)).map((user) => (
  <div key={user}>
    <img src={user.photoURL} referrerPolicy="no-referrer" alt="Profile Image" />
    <button>{user}</button>
  </div>
))}
</div>
    </ul>
  </div>
  <div class="messages">
    <div class="avatar">

    </div>
    </div>
    </div>
    </div>