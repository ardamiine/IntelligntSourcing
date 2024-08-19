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

    function openMenu() {
        hamburgerMenu.classList.add('active');
        flagMenu.style.display = 'block';
    }document.addEventListener('DOMContentLoaded', function() {
      const menuConfigs = [
        { hamburgerMenu: 'hamburger-menuTools1', flagMenu: 'tool-menuTools1', menuContainer: 'menuTools-container1' },
        { hamburgerMenu: 'hamburger-menuTools2', flagMenu: 'tool-menuTools2', menuContainer: 'menuTools-container2' },
        { hamburgerMenu: 'hamburger-menuTools3', flagMenu: 'tool-menuTools3', menuContainer: 'menuTools-container3' }
      ];
    
      menuConfigs.forEach(config => {
        const hamburgerMenu = document.getElementById(config.hamburgerMenu);
        const flagMenu = document.getElementById(config.flagMenu);
        const menuContainer = document.getElementById(config.menuContainer);
    
        function openMenu() {
            hamburgerMenu.classList.add('active');
            flagMenu.style.display = 'block';
        }
    
        function closeMenu() {
            hamburgerMenu.classList.remove('active');
            flagMenu.style.display = 'none';
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
    
        const flagItems = flagMenu.querySelectorAll('li');
        flagItems.forEach(item => {
            const img = item.querySelector('img');
            item.setAttribute('data-country', img.getAttribute('data-country'));
        });
      });
    });
    

    function closeMenu() {
        hamburgerMenu.classList.remove('active');
        flagMenu.style.display = 'none';
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

    const flagItems = flagMenu.querySelectorAll('li');
    flagItems.forEach(item => {
        const img = item.querySelector('img');
        item.setAttribute('data-country', img.getAttribute('data-country'));
    });
  });
});
