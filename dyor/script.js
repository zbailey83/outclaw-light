gsap.registerPlugin(ScrollTrigger);

const canvas = document.getElementById("scrub-canvas");
const context = canvas ? canvas.getContext("2d") : null;
const video = document.getElementById("hero-video");
const indicatorBar = document.getElementById("indicator-bar");
const cutLabel = document.getElementById("cut-label");
const frameCounter = document.getElementById("frame-counter");
const loaderOverlay = document.getElementById("loader-overlay");
const loaderText = document.getElementById("loader-text");
const loaderBar = document.getElementById("loader-bar");

const btnForward = document.getElementById("btn-autoscroll-forward");
const btnBackward = document.getElementById("btn-autoscroll-backward");

const frameCount = 240;
const currentFrame = index => `frames/frame_${index.toString().padStart(4, '0')}.webp`;

const images = [];
const airplay = { frame: 1 };
let timelineInitialized = false;
let autoScrollTween = null;
let useCanvas = true;

// Set 16:9 canvas dimensions matching 1920x1080 video scale
if (canvas) {
  canvas.width = 1920;
  canvas.height = 1080;
}

// Auto-Scroll helper functions using GSAP interpolation
function autoScrollForward() {
  if (autoScrollTween) autoScrollTween.kill();
  const maxScroll = ScrollTrigger.maxScroll(window);
  const scrollObj = { y: window.scrollY };
  
  autoScrollTween = gsap.to(scrollObj, {
    y: maxScroll,
    duration: 8,
    ease: "power1.inOut",
    onUpdate: () => {
      window.scrollTo(0, scrollObj.y);
    }
  });
}

function autoScrollBackward() {
  if (autoScrollTween) autoScrollTween.kill();
  const scrollObj = { y: window.scrollY };
  
  autoScrollTween = gsap.to(scrollObj, {
    y: 0,
    duration: 8,
    ease: "power1.inOut",
    onUpdate: () => {
      window.scrollTo(0, scrollObj.y);
    }
  });
}

window.addEventListener("wheel", () => {
  if (autoScrollTween) autoScrollTween.kill();
});
window.addEventListener("touchmove", () => {
  if (autoScrollTween) autoScrollTween.kill();
});

if (btnForward) btnForward.addEventListener("click", autoScrollForward);
if (btnBackward) btnBackward.addEventListener("click", autoScrollBackward);

// Draw current frame image onto canvas (object-fit: cover implementation)
function render() {
  const frameIndex = Math.min(frameCount, Math.max(1, Math.floor(airplay.frame)));
  
  if (frameCounter) {
    frameCounter.textContent = `FRAME // ${frameIndex.toString().padStart(3, '0')} / ${frameCount}`;
  }

  if (useCanvas && canvas && context) {
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
  } else if (video && video.duration) {
    const targetTime = ((frameIndex - 1) / (frameCount - 1)) * video.duration;
    if (Math.abs(video.currentTime - targetTime) > 0.04) {
      video.currentTime = targetTime;
    }
  }

  // Toggle autoscroll active indicator state
  if (frameIndex <= 10) {
    if (btnForward) btnForward.classList.add("active");
    if (btnBackward) btnBackward.classList.remove("active");
  } else if (frameIndex >= frameCount - 10) {
    if (btnBackward) btnBackward.classList.add("active");
    if (btnForward) btnForward.classList.remove("active");
  } else {
    if (btnForward) btnForward.classList.remove("active");
    if (btnBackward) btnBackward.classList.remove("active");
  }
}

function initInteractiveHero() {
  if (timelineInitialized) return;
  timelineInitialized = true;

  console.log("Initializing GSAP ScrollTrigger timeline for 240 frames.");

  // Master timeline pinned across 7500px scroll travel
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: ".hero-container",
      start: "top top",
      end: "+=7500",
      pin: true,
      scrub: 1.2,
      anticipatePin: 1,
      onUpdate: (self) => {
        if (indicatorBar) {
          indicatorBar.style.height = `${self.progress * 100}%`;
        }

        const currentFrameVal = self.progress * frameCount;
        if (cutLabel) {
          if (currentFrameVal < 70) {
            cutLabel.textContent = "AERIAL_DRIFT.01";
          } else if (currentFrameVal >= 70 && currentFrameVal < 140) {
            cutLabel.textContent = "PROFILE_PASS.02";
          } else if (currentFrameVal >= 140 && currentFrameVal < 195) {
            cutLabel.textContent = "CHASE_ZOOM.03";
          } else {
            cutLabel.textContent = "DESTINATION.04";
          }
        }
      }
    }
  });

  // 0. Scrub frame counter from 1 to 240
  tl.to(airplay, {
    frame: frameCount,
    ease: "none",
    duration: 10,
    onUpdate: render
  }, 0);

  // Card 1 Animation (Intro entry: frames 1 – 60, timeline 0 – 2.5)
  tl.set(".card-1", { autoAlpha: 1, y: 0 }, 0);
  tl.fromTo(".card-1 h2", 
    { letterSpacing: "0.2em", opacity: 0.5 }, 
    { letterSpacing: "0.35em", opacity: 1, duration: 1.5, ease: "power1.out" }, 
    0
  );
  tl.to(".card-1", {
    autoAlpha: 0,
    y: -40,
    duration: 0.8,
    ease: "power2.in"
  }, 2.0);

  // Card 2 Animation (Tech Specs HUD: frames 60 – 130, timeline 2.8 – 5.5)
  tl.fromTo(".card-2", 
    { autoAlpha: 0, y: 50, scale: 0.95 }, 
    { autoAlpha: 1, y: 0, scale: 1, duration: 0.8, ease: "back.out(1.4)" }, 
    2.8
  );

  const specBadges = document.querySelectorAll(".tech-spec-badge");
  tl.fromTo(specBadges,
    { opacity: 0, x: -30 },
    { opacity: 1, x: 0, duration: 0.6, stagger: 0.2, ease: "power2.out" },
    3.0
  );
  
  tl.fromTo(".card-2 .huge-letters",
    { opacity: 0.2, scale: 0.9 },
    { opacity: 1, scale: 1, duration: 1.0, ease: "power1.out" },
    3.4
  );

  tl.to(".card-2", {
    autoAlpha: 0,
    y: -40,
    scale: 0.95,
    duration: 0.8,
    ease: "power2.in"
  }, 5.0);

  // Card 3 Animation (Statement / Words: frames 130 – 195, timeline 5.5 – 7.8)
  tl.fromTo(".card-3", 
    { autoAlpha: 0, y: 40 }, 
    { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out" }, 
    5.5
  );

  const words = document.querySelectorAll(".card-3 .word");
  tl.fromTo(words,
    { opacity: 0, y: 30, filter: "blur(4px)" },
    { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.5, stagger: 0.18, ease: "power2.out" },
    5.8
  );

  tl.to(".card-3", {
    autoAlpha: 0,
    y: -40,
    duration: 0.6,
    ease: "power2.in"
  }, 7.4);

  // Card 4 Animation (Ending Climax & DYOR Button: frames 195 – 240, timeline 7.8 – 10)
  tl.fromTo(".card-4", 
    { autoAlpha: 0, y: 50, scale: 0.9 }, 
    { autoAlpha: 1, y: 0, scale: 1, duration: 0.8, ease: "back.out(1.7)" }, 
    7.8
  );

  tl.fromTo(".dyor-main-btn",
    { scale: 0.7, opacity: 0, boxShadow: "0 0 0px rgba(255, 69, 0, 0)" },
    { scale: 1, opacity: 1, boxShadow: "0 0 35px rgba(255, 69, 0, 0.6)", duration: 0.7, ease: "back.out(2)" },
    8.2
  );

  tl.fromTo(".sub-link",
    { opacity: 0, y: 15 },
    { opacity: 1, y: 0, duration: 0.5, ease: "power1.out" },
    8.7
  );
}

// Preload WebP frame sequence
let loadedCount = 0;
for (let i = 1; i <= frameCount; i++) {
  const img = new Image();
  img.src = currentFrame(i);
  
  img.onload = () => {
    loadedCount++;
    if (loaderText) {
      loaderText.textContent = `SYSTEM_LOAD // ${Math.round((loadedCount / frameCount) * 100)}%`;
    }
    if (loaderBar) {
      loaderBar.style.width = `${(loadedCount / frameCount) * 100}%`;
    }
    
    if (i === 1) render();

    if (loadedCount === frameCount) {
      if (loaderOverlay) {
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
      } else {
        initInteractiveHero();
      }
    }
  };

  img.onerror = () => {
    loadedCount++;
    if (loadedCount === frameCount) {
      // Fallback if some frames failed to load
      if (loaderOverlay) {
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
      } else {
        initInteractiveHero();
      }
    }
  };

  images.push(img);
}
