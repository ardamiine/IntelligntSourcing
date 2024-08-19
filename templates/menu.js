document.addEventListener("DOMContentLoaded", function() {
    function slideMenu() {
      var menuList = document.querySelector("#menu-container .menu-list");
      var activeState = menuList.classList.contains("active");
      menuList.style.left = activeState ? "0%" : "-100%";
    }
  
    document.querySelector("#menu-wrapper").addEventListener("click", function(event) {
      event.stopPropagation();
      document.querySelector("#hamburger-menu").classList.toggle("open");
      var menuList = document.querySelector("#menu-container .menu-list");
      menuList.classList.toggle("active");
      slideMenu();
      document.body.classList.toggle("overflow-hidden");
    });
  
    var accordionToggles = document.querySelectorAll(".menu-list .accordion-toggle");
    accordionToggles.forEach(function(toggle) {
      toggle.addEventListener("click", function() {
        var nextElement = this.nextElementSibling;
        nextElement.classList.toggle("open");
        nextElement.style.display = nextElement.classList.contains("open") ? "block" : "none";
        this.classList.toggle("active-tab");
        this.querySelector(".menu-link").classList.toggle("active");
  
        accordionToggles.forEach(function(otherToggle) {
          if (otherToggle !== toggle) {
            var otherNextElement = otherToggle.nextElementSibling;
            otherNextElement.classList.remove("open");
            otherNextElement.style.display = "none";
            otherToggle.classList.remove("active-tab");
            otherToggle.querySelector(".menu-link").classList.remove("active");
          }
        });
      });
    });
  });
  