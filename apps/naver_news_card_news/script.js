document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card-item');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    let currentIndex = 0;
    const totalCards = cards.length;

    function updateCards(index) {
        cards.forEach((card, i) => {
            if (i === index) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        });

        dots.forEach((dot, i) => {
            if (i === index) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    function nextCard() {
        currentIndex = (currentIndex + 1) % totalCards;
        updateCards(currentIndex);
    }

    function prevCard() {
        currentIndex = (currentIndex - 1 + totalCards) % totalCards;
        updateCards(currentIndex);
    }

    nextBtn.addEventListener('click', nextCard);
    prevBtn.addEventListener('click', prevCard);

    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            currentIndex = i;
            updateCards(currentIndex);
        });
    });

    // Keyboard Arrow Navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') {
            nextCard();
        } else if (e.key === 'ArrowLeft') {
            prevCard();
        }
    });

    // Touch Swipe Navigation for Mobile/Cards
    let touchStartX = 0;
    let touchEndX = 0;
    const stage = document.getElementById('cardStage');

    stage.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });

    stage.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        if (touchEndX < touchStartX - 40) {
            nextCard();
        }
        if (touchEndX > touchStartX + 40) {
            prevCard();
        }
    }

    // Fetch and populate news data
    fetch('news_data.json')
        .then(response => response.json())
        .then(data => {
            const cardMapping = {
                'economy-card': data.economy,
                'politics-card': data.politics,
                'culture-card': data.culture,
                'sports-card': data.sports,
                'society-card': data.society,
                'tech-card': data.tech,
                'world-card': data.world
            };

            for (const [cardClass, newsData] of Object.entries(cardMapping)) {
                const card = document.querySelector(`.${cardClass}`);
                if (card && newsData) {
                    card.querySelector('.news-title').innerHTML = newsData.title;
                    card.querySelector('.news-desc').textContent = newsData.desc;
                    
                    const ul = card.querySelector('.key-point-box ul');
                    ul.innerHTML = '';
                    newsData.points.forEach(point => {
                        const li = document.createElement('li');
                        li.textContent = point;
                        ul.appendChild(li);
                    });
                    
                    card.querySelector('.card-footer span').textContent = `출처: ${newsData.source} • ${newsData.category} 뉴스`;
                }
            }
        })
        .catch(error => console.error('Error fetching news data:', error));
});
});
