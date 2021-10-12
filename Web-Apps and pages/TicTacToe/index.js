var cube = document.getElementsByClassName("box");
let msg = document.querySelector(".msg");
let text = document.querySelector("p");
let section = document.querySelector("section");
let btn = document.querySelector("#btn")
var count = 0;
let turn = 1;

function func(ths)
{

    ths.classList.add("click-disable");
    count++;
    if (count % 2 == 0)
    {
        ths.innerHTML = "X";
        ths.accessKey = 1;
        turn = 1;
    } else
    {
        ths.innerHTML = "O";
        ths.accessKey = 0;
        turn = 2;
    }
    const a = parseInt(cube[0].accessKey);
    const b = parseInt(cube[1].accessKey);
    const c = parseInt(cube[2].accessKey);
    const d = parseInt(cube[3].accessKey);
    const e = parseInt(cube[4].accessKey);
    const f = parseInt(cube[5].accessKey);
    const g = parseInt(cube[6].accessKey);
    const h = parseInt(cube[7].accessKey);
    const i = parseInt(cube[8].accessKey);
    if (
        a + b + c == 3 ||
        d + e + f == 3 ||
        g + h + i == 3 ||
        a + d + g == 3 ||
        b + e + h == 3 ||
        c + f + i == 3 ||
        a + e + i == 3 ||
        c + e + g == 3
    )
    {
        text.innerHTML = `✨🎇 X won the match! 🎉🎊`;
        msg.style.visibility = "visible";
        section.style.pointerEvents = "none"
        setTimeout(() =>
        {
            restart();
        }, 4000);

    } else if (
        a + b + c == 0 ||
        d + e + f == 0 ||
        g + h + i == 0 ||
        a + d + g == 0 ||
        b + e + h == 0 ||
        c + f + i == 0 ||
        a + e + i == 0 ||
        c + e + g == 0

    )
    {
        text.innerHTML = `✨🎇 O won the match! 🎉🎊`;
        msg.style.visibility = "visible";
        section.style.pointerEvents = "none";
        setTimeout(() =>
        {
            restart();
        }, 4000);
    } else if (a + b + c + d + e + f + g + h + i)
    {
        text.innerHTML = `Match Draw !!!`;
        msg.style.visibility = "visible";
        section.style.pointerEvents = "none";
        setTimeout(() =>
        {
            restart();
        }, 4000);


    }
}
function restart() {
    document.location.reload();
}
