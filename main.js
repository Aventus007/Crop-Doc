const URL = "https://perenual.com/api/article-faq-list?key=sk-En9q66c87678a89126594&page=1"

const img = document.createElement('img')
const first = document.querySelector(".first")
const ques = document.querySelector(".second-a")
const ans = document.querySelector(".second-b")

function randomNum(){
    let num = Math.floor(Math.random()*30)
    return num
}

let num = randomNum()

async function makeAPICall() {
    const res = await fetch(URL)
    res.json().then(dt => {
        img.src = dt.data[num].default_image.regular_url
        first.appendChild(img)
        ques.innerHTML = dt.data[num].question
        ans.innerHTML = dt.data[num].answer
    })
}
makeAPICall()