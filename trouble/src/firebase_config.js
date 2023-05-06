// Import the functions you need from the SDKs you need
// import { initializeApp } from "firebase/compat/app";

import firebase from "firebase/compat/app";
import "firebase/compat/auth";
import {getFirestore} from 'firebase/firestore';


// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

import {getAuth, GoogleAuthProvider} from 'firebase/auth';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBRQpnXwizScLLCO4Cha6NwWi5c7rlz79M",
  authDomain: "chatapp-76a2c.firebaseapp.com",
  projectId: "chatapp-76a2c",
  storageBucket: "chatapp-76a2c.appspot.com",
  messagingSenderId: "856124496721",
  appId: "1:856124496721:web:aac069129576bf7cf91170"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();
export const database = getFirestore(app);


export default firebaseConfig;