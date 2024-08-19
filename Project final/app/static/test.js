document.addEventListener('DOMContentLoaded', function() {
    const hamburgermenuTools = document.getElementById('hamburger-menuTools');
    const toolmenuTools = document.getElementById('tool-menuTools');
    const menuToolsContainer = document.getElementById('menuTools-container');
  
    function openmenuTools() {
        hamburgermenuTools.classList.add('active');
        toolmenuTools.style.display = 'block';
    }
  
    function closemenuTools() {
        hamburgermenuTools.classList.remove('active');
        toolmenuTools.style.display = 'none';
    }
  
    hamburgermenuTools.addEventListener('click', function(event) {
        event.stopPropagation();
        if (toolmenuTools.style.display === 'none' || toolmenuTools.style.display === '') {
            openmenuTools();
        } else {
            closemenuTools();
        }
    });
  
    // Close menuTools when clicking outside
    document.addEventListener('click', function(event) {
        if (!menuToolsContainer.contains(event.target)) {
            closemenuTools();
        }
    });
  
    // Prevent menuTools from closing when clicking inside the tool menuTools
    toolmenuTools.addEventListener('click', function(event) {
        event.stopPropagation();
    });
  
    const toolItems = toolmenuTools.querySelectorAll('li');
    toolItems.forEach(item => {
        const img = item.querySelector('img');
        item.setAttribute('data-country', img.getAttribute('data-country'));
    });
  });