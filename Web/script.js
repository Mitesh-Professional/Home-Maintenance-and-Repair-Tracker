let user_name = document.getElementById('user_name')
let user_pass = document.getElementById('user_pass')
let user_birthdate = document.getElementById('user_birthdate')
let gender = document.getElementById('gender')
let from = document.querySelector('.form')
from.addEventListener('submit',(e)=>{
    e.preventDefault()
    eel.button_login(user_name.value, user_pass.value,user_birthdate.value,gender.value)
})