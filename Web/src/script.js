let user_name = document.getElementById('user_name')
let user_email = document.getElementById('user_email')
let user_pass = document.getElementById('user_pass')
let user_birthdate = document.getElementById('user_birthdate')
let gender = document.getElementById('gender')
let username = document.querySelector('#user_info_username')
let email = document.querySelector('#user_info_email')
let logo_inner_profile = document.querySelector('.profile_logo_text')
let profile = document.querySelector('.profile')

function onSubmit(e) {
    e.preventDefault()
    eel.button_signup(user_name.value, user_email.value, user_pass.value, user_birthdate.value, gender.value)(function (result) {
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
    eel.button_login(user_email.value, user_pass.value)(function (result) {
        if (!result.User_Verification) {
            alert(result.Info)
        }
        else {
            window.location.href = './home.html';
            alert(`Welcome To Home Maintenance and Repair Tracker, ${result.UserName}!`)
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
    console.log(logo_inner_profile)
    str = ""
    eel.user_profile_info()(function (result) {
        email.innerHTML = result.Email
        username.innerHTML = result.UserName
        logo_inner_profile.innerHTML = result.UserName.slice(0,2)
        profile.innerHTML = result.UserName.slice(0,2)
    })
}
function sing_out() {
    eel.sign_out()(function (result) {
        if (result) {
            window.location.href = './login_page.html';
        }
    })
}