document.addEventListener('DOMContentLoaded', function() {
    const menuConfigs = [
      { hamburgerMenu: 'hamburger-menuTools1', flagMenu: 'tool-menuTools1', menuContainer: 'menuTools-container1' },
      { hamburgerMenu: 'hamburger-menuTools2', flagMenu: 'tool-menuTools2', menuContainer: 'menuTools-container2' },
      { hamburgerMenu: 'hamburger-menuTools3', flagMenu: 'tool-menuTools3', menuContainer: 'menuTools-container3' }
    ];
  
    menuConfigs.forEach(config => {
      const hamburgerMenu = document.getElementById(config.hamburgerMenu);
      const flagMenu = document.getElementById(config.flagMenu);
      const menuContainer = document.getElementById(config.menuContainer);
      const up = document.getElementById('up');
      const down = document.getElementById('down');
  
      // Check if elements are found
      if (!hamburgerMenu || !flagMenu || !menuContainer || !up || !down) {
        console.warn('One or more elements are missing.');
        return; // Exit early if any of the elements are not found
      }
  
      function openMenu() {
        hamburgerMenu.classList.add('active');
        flagMenu.style.display = 'block';
        up.style.display = 'block';
        down.style.display = 'block';
      }
  
      function closeMenu() {
        hamburgerMenu.classList.remove('active');
        flagMenu.style.display = 'none';
        up.style.display = 'none';
        down.style.display = 'none';
      }
  
      hamburgerMenu.addEventListener('click', function(event) {
        event.stopPropagation();
        if (flagMenu.style.display === 'none' || flagMenu.style.display === '') {
          openMenu();
        } else {
          closeMenu();
        }
      });
  
      // Close menu when clicking outside
      document.addEventListener('click', function(event) {
        if (!menuContainer.contains(event.target)) {
          closeMenu();
        }
      });
  
      // Prevent menu from closing when clicking inside the flag menu
      flagMenu.addEventListener('click', function(event) {
        event.stopPropagation();
      });
  
      // Add scroll button functionality
      const scrollUpBtn = menuContainer.querySelector('.scroll-up');
      const scrollDownBtn = menuContainer.querySelector('.scroll-down');
  
      // Ensure scroll buttons exist before adding event listeners
      if (scrollUpBtn && scrollDownBtn) {
        scrollUpBtn.addEventListener('click', function() {
          flagMenu.scrollBy({
            top: -100, // Scroll up by 100px
            behavior: 'smooth'
          });
        });
  
        scrollDownBtn.addEventListener('click', function() {
          flagMenu.scrollBy({
            top: 100, // Scroll down by 100px
            behavior: 'smooth'
          });
        });
      } else {
        console.warn('Scroll buttons not found.');
      }
  
      const flagItems = flagMenu.querySelectorAll('li');
      flagItems.forEach(item => {
        const img = item.querySelector('img');
        if (img) {
          item.setAttribute('data-country', img.getAttribute('data-country'));
        }
      });
    });
  });
  

  