// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyD1KPhwXkZdRZM8YeV73iWjTa9XwNVlzzI",
    authDomain: "smart-dustbin-296ba.firebaseapp.com",
    databaseURL: "https://smart-dustbin-296ba-default-rtdb.firebaseio.com",
    projectId: "smart-dustbin-296ba",
    storageBucket: "smart-dustbin-296ba.appspot.com",
    messagingSenderId: "336746889319",
    appId: "1:336746889319:web:bc84e0988434d76ffdd4c2",
    measurementId: "G-7363DPF316"
  };
// Initialize Firebase
firebase.initializeApp(firebaseConfig);


function submitted(){
  let email=document.querySelector("#email").value
  let password=document.querySelector("#pass").value

 	firebase.auth().onAuthStateChanged((user) => {
  	if (user) {
    	// User is signed in, see docs for a list of available properties
    	// https://firebase.google.com/docs/reference/js/firebase.User
     	window.location.assign("index.html");
     	var uid = user.uid;
	   
	    // ...
  	} else {
	    // User is signed out
	    // ...
	    //window.location.assign("login.html");
  	}
	});

  firebase.auth().signInWithEmailAndPassword(email, password)
  .then((userCredential) => {
    // Signed in
    var user = userCredential.user;
    // ...
  })	
  .catch((error) => {
    var errorCode = error.code;
    var errorMessage = error.message;
    alert(errorMessage);
  });
}

function signUp(){
	window.location.assign("signup.html");
}