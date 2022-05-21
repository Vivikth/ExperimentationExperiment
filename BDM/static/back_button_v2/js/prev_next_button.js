// Source: https://www.jqueryscript.net/other/bootstrap-tabs-carousel.html
var useTab = true;
function bootstrapTabControl(){
  var i, items = $('.nav-link'), pane = $('.tab-pane');
  // next
    $('.nexttab').on('click', function(){

      for(i = 0; i < items.length; i++){
          if($(items[i]).hasClass('active') == true){
              break;
          }
      }
      if(i < items.length - 1){
          // for tab
          $(items[i]).removeClass('active');
          $(items[i+1]).addClass('active');
          // for pane
          $(pane[i]).removeClass('show active');
          $(pane[i+1]).addClass('show active');
      }

  });
  // Prev
  $('.prevtab').on('click', function(){
      for(i = 0; i < items.length; i++){
          if($(items[i]).hasClass('active') == true){
              break;
          }
      }
      if(i != 0){
          // for tab
          $(items[i]).removeClass('active');
          $(items[i-1]).addClass('active');
          // for pane
          $(pane[i]).removeClass('show active');
          $(pane[i-1]).addClass('show active');
      }
      });
}
bootstrapTabControl();


function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

function checkSubmit(btn) {
    buttonName = btn.name;
    let form = document.getElementById(buttonName);
    let isValid = form.reportValidity();
    if (!isValid) return;

    var formName = form.name;
    var formInput = form.value;
    var sendDict = {};

    if (formInput.length == 0) {
        alert("You must enter a switch-point");
        return;
    }

    var formValue = parseFloat(formInput);
    if (formValue < 0 || formValue > 100) {
        alert("Your switch-point must be between 0 and 100");
    } else if (formValue < 1 && formValue > 0) {
        if (confirm("Please double-check your switch-point. Remember that your switch-point is a percentage between 0 and 100. Press OK to proceed.")) {
            sendDict[formName] = formValue;
            liveSend(sendDict);
            document.getElementsByClassName("nexttab ".concat(btn.name))[0].click();
            topFunction();
        }
    } else {
        sendDict[formName] = formValue;
        liveSend(sendDict);
        document.getElementsByClassName("nexttab ".concat(btn.name))[0].click();
        topFunction();
    }
}

function liveRecv(data) {
    // your code goes here
    document.getElementById("Task1").innerHTML = data[0];
    document.getElementById("Task2").innerHTML = data[1];
    document.getElementById("Task3").innerHTML = data[2];
    document.getElementById("Task4").innerHTML = data[3];
    document.getElementById("Task5").innerHTML = data[4];
}
