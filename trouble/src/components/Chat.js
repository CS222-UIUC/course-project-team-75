import { useEffect, useState } from "react";
import {addDoc, collection, serverTimestamp, onSnapshot, query, where, orderBy} from "firebase/firestore"; //add messages to database
import { auth, database } from "../firebase_config";
import "../styles/Chat.css";

//Document in firstore= row from table, so here its a message from table
//props sends the room from App.js
export const Chat = (props) => {

    const {room} = props;

    //what user is typing into input
    const [newMessage, setNewMessage] = useState(""); //starte called new messaage and se tnew message
    //represnet what user is typing

    // Current user
    const currentUser = auth.currentUser;

    const [messages,setMessages] = useState([]);
    
    const messagesRef = collection(database, "messages");



    useEffect(() => {
        
        const queryMessages = query(messagesRef, 
            where("room","==",room),
            orderBy("createdAt"));
        
        const unsubscribe = onSnapshot(queryMessages, (snapshot) => {

            //console.log("NEW MESSAGE");

            let messages = [];
            
            snapshot.forEach((doc)=>{
                messages.push({...doc.data(),id:doc.id});
            });

            setMessages(messages);



        });


        //cleaning up useEffect?
        return () => unsubscribe();

    }, []);


    const handleSubmit = async (e) => {
        //so that submitting form, don't want page to reload
        e.preventDefault()
        if(newMessage === "")
        {return;}

        //adds messages to table
        await addDoc(messagesRef, {
            text: newMessage,
            createdAt: serverTimestamp(),
            user: auth.currentUser.displayName,
            photo: auth.currentUser.photoURL,
            room,

        });


        //setsmessage back to default, after u send a message u
        //dont want it to still be there
        setNewMessage("");



    };

    return (
    
    <div className="chat-app">
        <div className="header">
            <h1>Now talking to  {room.charAt(0).toUpperCase()} 
            {room.slice(1)} 
          </h1>

            

        </div>

        
            <div className="chat-messages">
  {messages.map((message) => (
    <div
      className={`message ${message.user === currentUser.displayName ? 'right' : ''}`}
      key={message.id}
    >
      <span className="user">
        <img
          className="profile-pic"
          src={message.photo}
          referrerPolicy="no-referrer"
          alt="https://www.library.illinois.edu/enx/wp-content/uploads/sites/27/2021/11/imageonline-co-roundcorner.png"
        />
        {message.user}
        <div className="messageText">{message.text}</div>
      </span>
    </div>
  ))}
</div>



        <form onSubmit = {handleSubmit} className="new-message-form">
            
            <input className="new-message-input" placeholder="Stir up Trouble..." 
            onChange={(e)=> setNewMessage(e.target.value)}
            value = {newMessage}/>
            <button type="submit" className="send-button">Send</button>


        </form>


    </div>
    
    
    );

}
