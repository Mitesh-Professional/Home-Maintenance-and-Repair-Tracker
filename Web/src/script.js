let user_name = document.getElementById('user_name')
let user_pass = document.getElementById('user_pass')
let user_birthdate = document.getElementById('user_birthdate')
let gender = document.getElementById('gender')
let from = document.querySelector('.form')
try {
    from.addEventListener('submit',(e)=>{
        e.preventDefault()
//        eel.button_signup(user_name.value, user_pass.value,user_birthdate.value,gender.value)
        eel.button_signup(user_name.value, user_pass.value,user_birthdate.value,gender.value)(function(result){
        if(!result){
        alert("Your Email ID already Exist!")}
        else{
        window.location.href = '../src/components/login_page.html';}})
    })
} catch (error) {
    let login = document.querySelector('.login')
    login.addEventListener('submit',(e)=>{
        e.preventDefault()
        eel.button_login(user_name.value,user_pass.value)
    })
}