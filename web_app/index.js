
// GENERATING TWO RANDOM NUMBER IN THE RANGE OF 1 AND 6
var randomnumber1 = (Math.floor(Math.random() * (6) + 1));
var randomnumber2 = (Math.floor(Math.random() * (6) + 1));

// COMPARISON AND DECLARING A WINNER
if(randomnumber1 > randomnumber2){
    document.querySelector("h1").innerHTML= "🚩Player 1 wins!";
}else if(randomnumber1 === randomnumber2){
    document.querySelector("h1").innerHTML= "Draw!";
}else{
    document.querySelector("h1").innerHTML= "🚩Player 2 wins!";
}

// MAKING THE IMAGES CHANGE ACCORDING TO THE DICE ROLL
var i1="images/dice" + randomnumber1 + ".png";
var i2="images/dice" + randomnumber2 + ".png";

// CHANGING THE TITLE BASED ON THE CONDITIONS
document.querySelector(".img1").setAttribute("src", i1);
document.querySelector(".img2").setAttribute("src", i2);
