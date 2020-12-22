var months_days = ["Jan",31,"Feb",29,"Mar",31,"Apr",30,"May",31,"Jun",30,"Jul",31,"Aug",31,"Sep",30,"Oct",31,"Nov",30,"Dec",31]

function fill_date_menus(){
    if (document.getElementById("dateform")){
        var month_menu = document.querySelector('#month');
        for (i = 0; i < months_days.length; i+=2) {
            var m_opt = document.createElement('option');
            m_opt.value = months_days[i];
            m_opt.innerHTML = months_days[i];
            month_menu.appendChild(m_opt);
        }
        change_days("month");
    }
}
function change_days(placeholder) {
    if (document.getElementById("dateform")){
        var day_menu = document.querySelector('#day');
        day_menu.options.length = 0;
        var value = document.querySelector('#'+placeholder).value;

        var month = months_days.indexOf(value);
        var days = months_days[month+1];

        //alert(value);
        for (i = 0; i < days; i++) {
            var d_opt = document.createElement('option');
            d_opt.value = i+1;
            d_opt.innerHTML = i+1;
            day_menu.appendChild(d_opt);
        }
    }
}
function today(b_date){
    //document.getElementById('date').value = b_date;
    if (document.getElementById("dateform")){
        document.getElementById("dateform").submit();
    }
}
function sortfield(field){
    document.getElementById("sortfield").value = field;
    //alert("about to submit");
    document.getElementById("compdate").submit();
}
function cksubmit(){
    if (document.getElementById("name1").value === '' || document.getElementById("name2").value === ''){
        document.getElementById("submit").disabled = true;
    } else {
        document.getElementById("submit").disabled = false;
    }
}
function change_zodiac(sign){
    if (sign == "z_sign") {
        document.getElementById('c_sign').style.display = "none";
        document.getElementById('z_sign').style.display = "inline-block";
        document.getElementById('z_signs').classList.remove("current");
        document.getElementById('c_signs').classList.add("current");
    } else {
        document.getElementById('c_sign').style.display = "inline-block";
        document.getElementById('z_sign').style.display = "none";
        document.getElementById('z_signs').classList.add("current");
        document.getElementById('c_signs').classList.remove("current");
    }
}
function change_sign(sign){
    document.getElementById("z_type").value = sign; //Astrological or Chinese?

    var label = document.getElementById(sign).selectedOptions[0].text;
    document.getElementById("z_name").value = label; //Send zodiac name!

    document.getElementById("z_form").submit();
}