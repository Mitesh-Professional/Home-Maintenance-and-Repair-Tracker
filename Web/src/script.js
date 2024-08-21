let user_name = document.getElementById('user_name')
let user_email = document.getElementById('user_email')
let user_pass = document.getElementById('user_pass')
let user_birthdate = document.getElementById('user_birthdate')
let gender = document.getElementById('gender')
let username = document.querySelector('#user_info_username')
let email = document.querySelector('#user_info_email')
let logo_inner_profile = document.querySelector('.profile_logo_text')
let profile = document.querySelector('.profile')
let main_ul = document.querySelector('.default_section_ul')
let objs = {
    'Plumbing': ['Leaks', 'Water Heater Maintenance', 'Drainage', 'Pipe Inspections'],
    'Electrical': ['Outlets and Switches', 'Smoke and Carbon Monoxide Detectors', 'Lighting Fixtures', 'Wiring and Circuit Breakers'],
    'HVAC (Heating, Ventilation, and Air Conditioning)': ['Furnace and Boiler Maintenance', 'Air Conditioning Units', 'Ventilation Systems', 'Filter Replacements'],
    'Roofing and Gutters': ['Roof Inspections', 'Gutter Cleaning and Repair', 'Downspouts', 'Flashing and Seals'],
    'Exterior Maintenance': ['Siding and Painting', 'Doors and Windows', 'Landscaping and Drainage', 'Exterior Lighting'],
    'Interior Maintenance': ['Walls and Ceilings', 'Cabinets and Countertops', 'Doors and Trim', 'Floors and Carpets'],
    'Safety and Security': ['Locks and Deadbolts', 'Emergency Preparedness', 'Fire Extinguishers', 'Security Systems'],
    'Pest Control': ['Inspections and Treatments', 'Rodent and Insect Control', 'Preventive Measures'],
    'Appliances': ['Kitchen Appliances', 'Repairs and Replacements', 'Regular Maintenance', 'Laundry Appliances'],
    'Seasonal Tasks': ['Spring Cleaning', 'Winterization', 'Summer Prep', 'Fall Maintenance']
}
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

for (obj in objs) {
    let create_main_li = document.createElement('li')
    let create_h2 = document.createElement('h2')
    let navbar_dropdown_ul = document.createElement('ul')
    create_main_li.className = 'li_repit'
    create_h2.innerHTML = obj
    create_main_li.appendChild(create_h2)
    navbar_dropdown_ul.className = 'ul_repit'
    main_ul.appendChild(create_main_li)
    for(value of objs[obj]){
        console.log(value)
        let create_li = document.createElement('li')
        create_li.className = 'default_product_list'
        create_li.innerHTML = value
        navbar_dropdown_ul.appendChild(create_li)
        create_main_li.appendChild(navbar_dropdown_ul)
    }
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
function dark_mode(){
    let toggle = document.querySelector('#check')
    let toggleSwitch = document.querySelector('#check')
    document.body.classList.toggle('dark-mode', toggleSwitch.checked);
    toggleSwitch.addEventListener('change',()=>{
        document.body.classList.toggle('dark-mode', toggleSwitch.checked);
    })
}