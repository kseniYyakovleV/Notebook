let change_password_button = document.getElementById("change_password_button");
let change_username_button = document.getElementById("change_username_button");
let delete_account_button = document.getElementById("delete_account_button");
let change_password_form = document.getElementById("change_password_form");
let change_username_form = document.getElementById("change_username_form");
let delete_account_form = document.getElementById("delete_account_form");


let old_password = document.getElementById("old_password");
let new_password1 = document.getElementById("new_password1");
let new_password2 = document.getElementById("new_password2");
let old_password_warning = document.getElementById("old_password_warning");
let new_password1_warning = document.getElementById("new_password1_warning");
let new_password2_warning = document.getElementById("new_password2_warning");


let username = document.getElementById("username");
let username_warning = document.getElementById("username_warning");





change_password_button.addEventListener("click", e=>{
    change_password_form.hidden = false;
    change_username_form.hidden = true;
    delete_account_form.hidden = true;
})

change_username_button.addEventListener("click", e=>{
    change_password_form.hidden = true;
    change_username_form.hidden = false;
    delete_account_form.hidden = true;
})

delete_account_button.addEventListener("click", e=>{
    change_password_form.hidden = true;
    change_username_form.hidden = true;
    delete_account_form.hidden = false;
})

function old_password_is_valid() {
    if (old_password.value.length == 0) {
        return false;
    }
    else {
        return true;
    }
}

function new_password1_is_valid() {
    let value = new_password1.value;
    let int_value = parseInt(value);
    if (new_password1.value.length >= 8 & value!=int_value.toString()) {
        return true;
    }
    else {
        return false;
    }
}

function new_password2_is_valid() {
    if (new_password1.value == new_password2.value) {
        return true;
    } else {
        return false;
    }
}

function new_username_is_valid() {
    let value = username.value;
    if (value.length == 0) {
        return false;
    }
    for (let index = 0; index < value.length; index++) {
        if (value[index].match("[a-zA-Z0-9]") == null) {
            return false;
        }
    }
    return true;
}

old_password.addEventListener("input", e=>{
    old_password_warning.hidden = old_password_is_valid();
})


new_password1.addEventListener("input", e=>{
    new_password1_warning.hidden = new_password1_is_valid();
})


new_password2.addEventListener("input", e=>{
    new_password2_warning.hidden =new_password2_is_valid();
})

username.addEventListener("input", e=>{
    username_warning.hidden = new_username_is_valid();
})
