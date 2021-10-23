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

firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        var uid = user.uid;
    } else {
        window.location.assign("login.html");
    }
});

//temp firebase data
let status = firebase.database().ref("Active");

// this function is helping to update data from firebase at real time 
status.on("value", function(snapshot) {
    let st = snapshot.val();
    // # for id
    document.querySelector("#status").innerHTML = st;
})

//light firebase data
let light = firebase.database().ref("Level-of-Bin/Value");

// this function is helping to update data from firebase at real time 
light.on("value", function(snapshot) {
    if (snapshot.val() == 0)
        document.querySelector("#image").src = "0.jpg";
    else if(snapshot.val() == 25)
        document.querySelector("#image").src = "25.jpg";
    else if(snapshot.val() == 50)
        document.querySelector("#image").src = "50.jpg";
    else
        document.querySelector("#image").src = "100.jpg";
})

//temp firebase data
let temp = firebase.database().ref("Level-of-Bin/Value");

// this function is helping to update data from firebase at real time 
temp.on("value", function(snapshot) {
    let tempvalue = snapshot.val();
    // # for id
    document.querySelector("#tempout").innerHTML = tempvalue;
})

function signout() {
    // [START auth_sign_out]
    firebase.auth().signOut().then(() => {
        console.log("Sign-out successful")
    }).catch((error) => {
        var errorMessage = error.message;
        alert(errorMessage);
        console.log("sign out not successful")
    });
    // [END auth_sign_out]
}