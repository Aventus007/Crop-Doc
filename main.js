const radio_btn = document.querySelectorAll('input')

let i = 1
setInterval(() => {
    radio_btn[i].checked=true
    i=(i+1)%radio_btn.length
}, 4000);