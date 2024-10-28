let period = document.getElementById("period");
let period_days = document.getElementsByClassName("period_days")[0];
let duration = document.getElementById("duration"); 
let duration_days = document.getElementsByClassName("duration_days")[0];
let period_container = document.getElementById("period_container");
let start_datetime = document.getElementById("start_time");
let end_datetime = document.getElementById("end_time");
let interval_error = document.getElementById("interval_error");
let period_error = document.getElementById("period_error");
let description = document.getElementById("description");

const MAX = 365;
const MIN = 1;



function Date_to_datetime(date) {
    year = date.getFullYear().toString().padStart(4, '0');
    month = (date.getMonth()+1).toString().padStart(2, '0');
    day = date.getDate().toString().padStart(2, '0');
    hours = date.getHours().toString().padStart(2, '0');
    minutes = date.getMinutes().toString().padStart(2, '0');

    datetime_str = year + '-' + month + '-' + day + "T" + hours + ':' + minutes;
    return datetime_str;
}



period.addEventListener('input', e => {
    let value = parseInt(duration.value);
    let period_value = parseInt(period.value)

    if (period_value > MAX) {
        period.value = 365;
    } else if (period_value < MIN & period_value != "") {
        period.value = MIN;
    }
    let end = period_value%10;
    let two_digits = period_value%100;
    if (period_value == "") {
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

    if (period_value < value) {
        period_error.hidden = false;
        duration.value = period_value;
    } else {
        period_error.hidden = true;
    }
})


duration.addEventListener('input', e => {
    let value = parseInt(duration.value);
    let period_value = parseInt(period.value)

    if (value > MAX) {
        duration.value = 365;
    } else if (value < MIN & value != "") {
        duration.value = MIN;
    }
    let end = value%10;
    let two_digits = value%100;
    if (value == "") {
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

    if (period_value < value) {
        period_error.hidden = false;
        duration.value = period_value;
    } else {
        period_error.hidden = true;
    }
})


let periodic_checkbox = document.getElementById("periodic");
let periodic_container = document.getElementById("periodic_container");

periodic_checkbox.addEventListener("change", e =>{
    let a = periodic_container.hidden;
    periodic_container.hidden = !periodic_container.hidden;
})


end_datetime.addEventListener("change", e=>{
    start_time = new Date(start_datetime.value);
    end_time = new Date(end_datetime.value);
    console.log(Date_to_datetime(end_time))
    if ((end_time.getTime() - start_time.getTime()) < 86400000) {
        interval_error.hidden = false;
        end_time.setTime(start_time.getTime() + 86400000);
        str_time = Date_to_datetime(end_time);
        end_datetime.value = str_time;
    } else {
        interval_error.hidden = true;
    }
})

start_datetime.addEventListener("change", e=>{
    start_time = new Date(start_datetime.value);
    end_time = new Date(end_datetime.value);
    console.log(Date_to_datetime(end_time))
    if ((end_time.getTime() - start_time.getTime()) < 86400000) {
        interval_error.hidden = false;
        end_time.setTime(start_time.getTime() + 86400000);
        str_time = Date_to_datetime(end_time);
        end_datetime.value = str_time;
    } else {
        interval_error.hidden = true;
    }
})

interval_error.addEventListener("click", e=>{   
    interval_error.hidden = true;
})

period_error.addEventListener("click", e=>{   
    period_error.hidden = true;
})


description.addEventListener("input", e=>{
    len = description.value.length;
    if(len === 0) {
        description.value = " ";
    }
})