// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore"; // Import Firestore

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA-n8vLITo_RIbKGK65Y9BSam9L9yfxCk0",
  authDomain: "cher-19625.firebaseapp.com",
  projectId: "cher-19625",
  storageBucket: "cher-19625.appspot.com",
  messagingSenderId: "483334156837",
  appId: "1:483334156837:web:b41da1b52e38cadc5605cc",
  measurementId: "G-RN6RJSCYPB",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app); // Initialize Firestore

export { db };
