let period = document.getElementById("period");
let period_days = document.getElementsByClassName("period_days")[0];
let duration = document.getElementById("duration"); 
let duration_days = document.getElementsByClassName("duration_days")[0];
let period_container = document.getElementById("period_container");

const MAX = 365;
const MIN = 1;

period.addEventListener('input', e => {
    if (e.target.value > MAX) {
        e.target.value = 365;
    } else if (e.target.value < MIN & e.target.value != "") {
        e.target.value = MIN;
    }
    let value = e.target.value
    let end = value%10;
    let two_digits = value%100;
    if (e.target.value == "") {
    } else if (end == 1) {
        if (two_digits == 11) {
            period_days.textContent = "дней";
        } else {
            period_days.textContent = "день";
        }
    } else if (end == 2 | end == 3 | end ==4){
        if (two_digits == 12 | two_digits == 13 | two_digits==14) {
            period_days.textContent = "дней";
        } else {
            period_days.textContent = "дня";
        }
    } else if (end == 5 | end == 6 | end == 7 | end == 8 | end == 9 | end == 0) {
        period_days.textContent = "дней";
    }
})


duration.addEventListener('input', e => {
    if (e.target.value > MAX) {
        e.target.value = 365;
    } else if (e.target.value < MIN & e.target.value != "") {
        e.target.value = MIN;
    }
    let value = e.target.value
    let end = value%10;
    let two_digits = value%100;
    if (e.target.value == "") {
    } else if (end == 1) {
        if (two_digits == 11) {
            duration_days.textContent = "дней";
        } else {
            duration_days.textContent = "день";
        }
    } else if (end == 2 | end == 3 | end ==4){
        if (two_digits == 12 | two_digits == 13 | two_digits==14) {
            duration_days.textContent = "дней";
        } else {
            duration_days.textContent = "дня";
        }
    } else if (end == 5 | end == 6 | end == 7 | end == 8 | end == 9 | end == 0) {
        duration_days.textContent = "дней";
    }
})


let periodic_checkbox = document.getElementById("periodic");
let periodic_container = document.getElementById("periodic_container");

periodic_checkbox.addEventListener("change", e =>{
    let a = periodic_container.hidden;
    periodic_container.hidden = !periodic_container.hidden;
})