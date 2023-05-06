//import logo from './logo.svg';
import './App.css';
import React, { useState, useRef, useEffect } from "react";
import {Auth} from "./components/Auth";
import {Chat} from "./components/Chat";
import {signOut} from "firebase/auth";
import {auth} from "./firebase_config";


import {getDocs, doc, collection, onSnapshot, query, where, orderBy} from "firebase/firestore"; //add messages to database
import _ from "lodash";
import { database } from "./firebase_config";

import Cookies from 'universal-cookie';
const cookies = new Cookies();

const currentUser = auth.currentUser;

function App() {

  const [isAuth, setIsAuth] = useState(cookies.get("auth-token"));
  const [room, setRoom] = useState(null);

  const roomInputRef = useRef(null);

    // Current user  

    const [usersList,setusersList] = useState([]);
 
    
    const roomsRef = collection(database, "messages");
    //console.log(currentUserRooms);


  useEffect(() => {
  

  const fetchUsers = async () => {
    const messagesCollection = collection(database, "messages");
    const querySnapshot = await getDocs(messagesCollection);
    const users = {};

    

    querySnapshot.forEach((doc) => {
      const user = doc.data().user;
      const message = {
        createdAt: doc.data().createdAt,
        room: doc.data().room,
        text: doc.data().text,
      };

      // If the user has not been seen before, add them to the object
      if (!users[user] && user !== "undefined") {
        users[user] = {
          photo: doc.data().photo,
          messages: [message],
        };
      } else {
        // Otherwise, add the message to the user's existing messages array
        users[user].messages.push(message);
      }
  

    });

  


    // Sort the messages for each user by createdAt in descending order
    for (const user in users) {
      users[user].messages.sort((a, b) =>
        a.createdAt > b.createdAt ? -1 : 1
      );
    }

    const uniqueUsers = Object.keys(users).map((user) => ({
      name: user,
      photo: users[user].photo,
      latestMessage: users[user].messages[0],
    }));

    
    setusersList(uniqueUsers);
    
  };



  fetchUsers();
}, []);





  


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

<div className = "sign-out">
        <button onClick={signUserOut}>Sign Out</button>
    </div>
        <div className="header">
       
      <div>Trou<span>ble</span></div>
      <img
        className="logo"
        src={require('./output_onlinepngtools.png')}
        alt="gay man walking susical"
      />
      
    </div>

    
    <body>
  
    <div class="container">

<div class="side">
  <div class="menu">
    <ul>
      
      <li class="active">Messages</li>
    </ul>


  </div>


 
  
 
  {usersList.filter(user => user.name !== "undefined").map((user) => (
    
    <div key={user.name}>
      {user.photo && (
        <div class="avatar">
          <img src={user.photo} referrerPolicy="no-referrer" alt="Profile Image"/>
        </div>
      )}
   
   <p> 
      <div class="message">

      <div class="user">
        {user.name && (
          <div>{user.name}</div>
        )}
        </div>
        <div class="text">
        {user.latestMessage && user.latestMessage.text && (
          <div>{user.latestMessage.text}</div>
        )}
        </div>
      </div>

      </p> 
      </div>



  ))}
  




  </div>
  <p> {room ? <Chat room = {room}/> :
    
    <div className='room'>
      
      <label>Who would you like to talk with?</label>
      <input ref = {roomInputRef}/>
      <button onClick={() => setRoom(roomInputRef.current.value)}>Enter Chat</button>

    </div>

    }
  </p>
  </div>


  </body>
  

   

  </div>

  
  
  );

}

export default App;




