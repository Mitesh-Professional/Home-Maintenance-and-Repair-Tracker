let user_name = document.getElementById('user_name')
let user_pass = document.getElementById('user_pass')
let user_birthdate = document.getElementById('user_birthdate')
let gender = document.getElementById('gender')
let email = document.querySelector('#user_name_value')
function onSubmit(e) {
    e.preventDefault()
    eel.button_signup(user_name.value, user_pass.value, user_birthdate.value, gender.value)(function (result) {
        if (!result) {
            alert("Your Email ID already Exist!")
        }
        else {
            window.location.href = '../src/components/login_page.html';
        }
    })
}
function onLogin(e) {
    e.preventDefault()
    eel.button_login(user_name.value, user_pass.value)(function (result) {
        if (!result.Status) {
            alert("Your Email and Password Wrong!")
        }
        else {
            window.location.href = './home.html';
            alert("Welcome, Home Maintenance and Repair Tracker"
            )
        }
    })
}
function card_view() {
    let display_value = document.getElementsByClassName('profile_view')
    if (window.getComputedStyle(display_value[0]).display == 'none') {
        display_value[0].style.display = 'block'
    } else {
        display_value[0].style.display = 'none'
    }
}
if ("http://localhost:8000/src/components/home.html" == window.location.href) {
    eel.user_profile_info()(function (result) {
       email.innerHTML = result.Email
    })
}