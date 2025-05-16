// Import the functions you need from the SDKs you need
import { getAuth, GoogleAuthProvider,signOut  } from "firebase/auth";
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAEKnElgT4jQ0vMggrtqmi6YoWICp1V63Q",
  authDomain: "contract-1f93a.firebaseapp.com",
  projectId: "contract-1f93a",
  storageBucket: "contract-1f93a.firebasestorage.app",
  messagingSenderId: "373205286572",
  appId: "1:373205286572:web:217196966e6a010b15a909",
  measurementId: "G-SFN9WH5J8K"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();


export { auth, provider,signOut  };