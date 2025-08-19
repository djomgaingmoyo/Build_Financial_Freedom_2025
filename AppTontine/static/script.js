// Carousel functionality
            document.addEventListener('DOMContentLoaded', function() {
                const items = document.querySelectorAll('.carousel-item');
                const indicators = document.querySelectorAll('.indicator');
                let currentIndex = 0;
                
                // Show initial item
                showItem(currentIndex);
                
                // Next button
                document.getElementById('nextBtn').addEventListener('click', function() {
                    currentIndex = (currentIndex + 1) % items.length;
                    showItem(currentIndex);
                });
                
                // Previous button
                document.getElementById('prevBtn').addEventListener('click', function() {
                    currentIndex = (currentIndex - 1 + items.length) % items.length;
                    showItem(currentIndex);
                });
                
                // Indicators
                indicators.forEach(indicator => {
                    indicator.addEventListener('click', function() {
                        currentIndex = parseInt(this.getAttribute('data-index'));
                        showItem(currentIndex);
                    });
                });
                
                // Auto-rotate every 5 seconds
                setInterval(() => {
                    currentIndex = (currentIndex + 1) % items.length;
                    showItem(currentIndex);
                }, 5000);
                
                function showItem(index) {
                    // Hide all items
                    items.forEach(item => {
                        item.classList.remove('visible');
                        item.classList.add('hidden');
                    });
                    
                    // Show selected item
                    items[index].classList.remove('hidden');
                    items[index].classList.add('visible');
                    
                    // Update indicators
                    indicators.forEach((indicator, i) => {
                        if (i === index) {
                            indicator.classList.remove('bg-orange-300');
                            indicator.classList.add('bg-orange-600');
                        } else {
                            indicator.classList.remove('bg-orange-600');
                            indicator.classList.add('bg-orange-300');
                        }
                    });
                }

                // Update copyright year dynamically
                document.getElementById('current-year').textContent = new Date().getFullYear();
            });