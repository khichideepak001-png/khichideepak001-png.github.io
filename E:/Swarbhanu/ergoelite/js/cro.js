document.addEventListener('DOMContentLoaded', () => {
  /* ========================================================================
     1. Social Proof Toasts
     ======================================================================== */
  
  // Data for the social proof notifications
  const products = [
    { name: "Herman Miller Aeron", img: "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=100&q=80" },
    { name: "Steelcase Leap V2", img: "https://images.unsplash.com/photo-1595514535415-ebfb2d1e4eb4?w=100&q=80" },
    { name: "FlexiSpot E7 Pro", img: "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=100&q=80" },
    { name: "Uplift V2 Standing Desk", img: "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=100&q=80" },
    { name: "Branch Ergonomic Chair", img: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=100&q=80" }
  ];
  
  const locations = ["New York", "London", "Austin", "Chicago", "Toronto", "Sydney", "Seattle", "Berlin"];
  const names = ["Sarah", "Michael", "David", "Emma", "James", "Olivia", "Alex", "Chris"];
  const times = ["2 minutes ago", "Just now", "5 minutes ago", "12 minutes ago", "1 hour ago"];

  // Create the toast element
  const toast = document.createElement('div');
  toast.className = 'social-proof-toast';
  toast.innerHTML = `
    <img src="" alt="Product" class="sp-img">
    <div class="sp-content">
      <div class="sp-title"></div>
      <div class="sp-time"></div>
    </div>
  `;
  document.body.appendChild(toast);

  const imgEl = toast.querySelector('.sp-img');
  const titleEl = toast.querySelector('.sp-title');
  const timeEl = toast.querySelector('.sp-time');

  function showNextToast() {
    // Pick random data
    const product = products[Math.floor(Math.random() * products.length)];
    const location = locations[Math.floor(Math.random() * locations.length)];
    const name = names[Math.floor(Math.random() * names.length)];
    const time = times[Math.floor(Math.random() * times.length)];

    imgEl.src = product.img;
    titleEl.innerHTML = `<strong>${name}</strong> from ${location} purchased<br><span class="text-accent">${product.name}</span>`;
    timeEl.textContent = time;

    toast.classList.add('show');

    // Hide after 5 seconds
    setTimeout(() => {
      toast.classList.remove('show');
    }, 5000);

    // Schedule next toast between 15 and 35 seconds
    const nextDelay = Math.floor(Math.random() * 20000) + 15000;
    setTimeout(showNextToast, nextDelay);
  }

  // Start the toast sequence after 5 seconds
  setTimeout(showNextToast, 5000);


  /* ========================================================================
     2. Exit-Intent Popup
     ======================================================================== */
  
  let exitIntentTriggered = false;

  // Create the modal element
  const exitModal = document.createElement('div');
  exitModal.className = 'exit-modal-overlay';
  exitModal.innerHTML = `
    <div class="exit-modal">
      <button class="exit-close" aria-label="Close">&times;</button>
      <h2>Wait! Don't buy yet.</h2>
      <p>Get our free <strong>2026 Ergonomic Setup Guide</strong>. Avoid the 3 biggest mistakes people make when buying home office gear.</p>
      <form class="exit-form" id="exitForm" action="#" method="POST">
        <input type="email" class="exit-input" placeholder="Enter your email address" required>
        <button type="submit" class="btn btn-primary w-full">Send Me The Free Guide</button>
      </form>
    </div>
  `;
  document.body.appendChild(exitModal);

  const closeBtn = exitModal.querySelector('.exit-close');
  const form = exitModal.querySelector('#exitForm');

  function showExitModal() {
    if (exitIntentTriggered) return;
    
    // Check if they already closed it this session
    if (sessionStorage.getItem('exitModalShown')) return;

    exitIntentTriggered = true;
    sessionStorage.setItem('exitModalShown', 'true');
    exitModal.classList.add('show');
  }

  function hideExitModal() {
    exitModal.classList.remove('show');
  }

  // Trigger on mouse leave (top of viewport)
  document.addEventListener('mouseout', (e) => {
    if (e.clientY < 20) {
      showExitModal();
    }
  });

  // Close modal on click of X or overlay
  closeBtn.addEventListener('click', hideExitModal);
  exitModal.addEventListener('click', (e) => {
    if (e.target === exitModal) {
      hideExitModal();
    }
  });

  // Handle form submission (placeholder for now)
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button');
    btn.textContent = 'Success! Check your inbox.';
    btn.style.background = 'var(--emerald)';
    btn.style.color = '#fff';
    
    setTimeout(() => {
      hideExitModal();
    }, 2000);
  });
});
