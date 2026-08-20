gsap.registerPlugin(ScrollTrigger);

const canvas = document.getElementById("scrub-canvas");
const context = canvas.getContext("2d");
const loaderOverlay = document.getElementById("loader-overlay");
const loaderText = document.getElementById("loader-text");
const loaderBar = document.getElementById("loader-bar");

const frameCount = 192; // Total frames for video 3
const currentFrame = index => `frames3/frame_${index.toString().padStart(3, '0')}.webp`;

const images = [];
const airplay = { frame: 1 };
let timelineInitialized = false;

// Set dimensions to match 1280x720 landscape video
canvas.width = 1280;
canvas.height = 720;

// Draw current frame to canvas using CSS object-fit: cover logic
function render() {
  const frameIndex = Math.min(frameCount, Math.max(1, Math.floor(airplay.frame)));
  const img = images[frameIndex - 1];
  
  if (img && img.complete) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    
    const imgRatio = img.width / img.height;
    const canvasRatio = canvas.width / canvas.height;
    let drawWidth, drawHeight, drawX, drawY;

    if (imgRatio > canvasRatio) {
      drawHeight = canvas.height;
      drawWidth = canvas.height * imgRatio;
      drawX = (canvas.width - drawWidth) / 2;
      drawY = 0;
    } else {
      drawWidth = canvas.width;
      drawHeight = canvas.width / imgRatio;
      drawX = 0;
      drawY = (canvas.height - drawHeight) / 2;
    }

    context.drawImage(img, drawX, drawY, drawWidth, drawHeight);
  }
}

function initInteractiveHero() {
  if (timelineInitialized) return;
  timelineInitialized = true;

  console.log("Timeline Variation 3 initialized. Frame count:", frameCount);

  // Pinned Master timeline across 7500px scroll travel
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: ".hero-container",
      start: "top top",
      end: "+=7500",
      pin: true,
      scrub: 1.2, // Smooth inertia
      anticipatePin: 1
    }
  });

  // Smooth floating point frame tween
  tl.to(airplay, {
    frame: frameCount,
    ease: "none",
    duration: 10,
    onUpdate: render
  }, 0);

  // Card 1 Animation (Intro entry: timeline 0 – 3.3, frames 1 - 63)
  tl.set(".card-1", { autoAlpha: 1, y: 0 }, 0);
  tl.fromTo(".card-1 h2", 
    { letterSpacing: "0.2em", opacity: 0.5 }, 
    { letterSpacing: "0.35em", opacity: 1, duration: 1.5, ease: "power1.out" }, 
    0
  );
  tl.to(".card-1", {
    autoAlpha: 0,
    y: -30,
    duration: 0.8,
    ease: "power2.in"
  }, 2.5);

  // Card 2 Animation (Middle Turnaround spin climax: timeline 3.7 – 6.3)
  // Activates in the middle as the car turns around, featuring 1st Etsy CTA
  tl.fromTo(".card-2", 
    { autoAlpha: 0, y: 40, scale: 0.95 }, 
    { autoAlpha: 1, y: 0, scale: 1, duration: 0.8, ease: "back.out(1.5)" }, 
    3.7
  );
  
  tl.fromTo(".card-2 .letter-stroke",
    { opacity: 0.3 },
    { opacity: 1, duration: 1.0 },
    3.9
  );

  tl.to(".card-2", {
    autoAlpha: 0,
    y: -40,
    duration: 0.8,
    ease: "power2.in"
  }, 5.8);

  // Card 3 Animation (End frame climax: timeline 5.8 – 10)
  // Positioned in bottom-right corner to present 2nd Etsy CTA
  tl.fromTo(".card-3", 
    { autoAlpha: 0, y: 40 }, 
    { autoAlpha: 1, y: 0, duration: 0.8, ease: "power2.out" }, 
    5.8
  );

  const words = document.querySelectorAll(".card-3 .word");
  tl.fromTo(words,
    { opacity: 0, y: 25 },
    { opacity: 1, y: 0, duration: 0.6, stagger: 0.15, ease: "power2.out" },
    6.2
  );

  tl.fromTo(".card-3 .cta-btn",
    { scale: 0.85, opacity: 0 },
    { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(2)" },
    6.8
  );
}

// Preload frames and run page
let loadedCount = 0;
for (let i = 1; i <= frameCount; i++) {
  const img = new Image();
  img.src = currentFrame(i);
  img.onload = () => {
    loadedCount++;
    
    if (loaderText) {
      loaderText.textContent = `LOADING // ${Math.round((loadedCount / frameCount) * 100)}%`;
    }
    if (loaderBar) {
      loaderBar.style.width = `${(loadedCount / frameCount) * 100}%`;
    }
    
    if (i === 1) {
      render();
    }

    if (loadedCount === frameCount) {
      gsap.to(loaderOverlay, {
        autoAlpha: 0,
        duration: 0.8,
        ease: "power2.out",
        onComplete: () => {
          document.body.classList.remove("loading");
          loaderOverlay.style.display = "none";
          initInteractiveHero();
          ScrollTrigger.refresh();
        }
      });
    }
  };

  img.onerror = () => {
    loadedCount++;
    if (loadedCount === frameCount) {
      gsap.to(loaderOverlay, {
        autoAlpha: 0,
        duration: 0.8,
        onComplete: () => {
          document.body.classList.remove("loading");
          loaderOverlay.style.display = "none";
          initInteractiveHero();
          ScrollTrigger.refresh();
        }
      });
    }
  };
  
  images.push(img);
}
