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
let periodic_checkbox = document.getElementById("periodic");
let periodic_container = document.getElementById("periodic_container");
let title_input = document.getElementById("title");
let title_error = document.getElementById("title_error");
let type_error = document.getElementById("type_error");
let date_format_error = document.getElementById("date_format_error");

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


function is_title_valid() {
    let value = title_input.value;
    let bad_start = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c0123456789';
    if (value.length > 0) {
        if (bad_start.includes(value[0])) {
            return false;
        } else {
            return true;
        }
    } else {
        return false;
    }
}



function is_deadlines_valid() {
    start_time = new Date(start_datetime.value);
    end_time = new Date(end_datetime.value);
    if (end_time.getTime() <= start_time.getTime()) {
        return false;
    } else {
        return true;
    }
}

function is_period_types_valid() {
    let execution_value = parseInt(duration.value);
    let period_value = parseInt(period.value);
    if (period_value != parseFloat(period.value) | execution_value != parseFloat(duration.value)) { return false; }
    if (duration.value == "" | period.value == "") { return false; }
    if (execution_value == 0 | period_value == 0) { return false; }
    return true;
}

function is_period_values_valid() {
    let execution_value = parseInt(duration.value);
    let period_value = parseInt(period.value);
    if (period_value < execution_value) { return false; } 
    return true;
}


function is_datetime_format_valid() {
    let start_datetime = document.getElementById("start_time");
    let end_datetime = document.getElementById("end_time");
    if (start_datetime.value == "" | end_datetime.value == "") { return false; }
    return true;
}

function period_days_check() {
    let value = parseInt(duration.value);
    let period_value = parseInt(period.value)

    if (period_value > MAX) {
        period.value = 365;
    } else if (period_value < MIN & period_value != "") {
        period.value = MIN;
    }
    let end = period_value%10;
    let two_digits = period_value%100;
    if (period_value === "") {
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
    
    type_error.hidden = is_period_types_valid();
    period_error.hidden = is_period_values_valid();
   
}


function duration_days_check() {
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

    type_error.hidden = is_period_types_valid();
    if (is_period_types_valid) { period_error.hidden = is_period_values_valid(); }
    
}

period_days_check();
duration_days_check();




title_input.addEventListener('input', e => {
    title_error.hidden = is_title_valid();
})

period.addEventListener('input', e => {
    period_days_check();
    console.log("period")
})



duration.addEventListener('input', e => {
    console.log("duration");
    duration_days_check();
})



periodic_checkbox.addEventListener("change", e =>{
    if (e.target.checked) {
        e.target.value = "True"
    } else {
        e.target.value = "False"
    }
    let a = periodic_container.hidden;
    periodic_container.hidden = !periodic_container.hidden;
})


end_datetime.addEventListener("change", e=>{
    interval_error.hidden = is_deadlines_valid();
    date_format_error.hidden = is_datetime_format_valid()
})

start_datetime.addEventListener("change", e=>{
    interval_error.hidden = is_deadlines_valid();
    date_format_error.hidden = is_datetime_format_valid()
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



