    // JavaScript to add the "active" class to the clicked link
    var links = document.querySelectorAll('.navbar a');
    links.forEach(function(link) {
        link.addEventListener('click', function() {
            links.forEach(function(l) {
                l.classList.remove('active');
            });
            this.classList.add('active');
        });
    });