import "../App.css";
import { useEffect, useRef, useState } from "react";
import logo from "../assets/logo.png";

function LandingPage({ onSwipeUp }) {
  const startY = useRef(0);
  const [canSwipe, setCanSwipe] = useState(false);

  // Enable swipe only after bot animation completes
  useEffect(() => {
    const timer = setTimeout(() => {
      setCanSwipe(true);
    }, 9000); // SAME duration as bot animation

    return () => clearTimeout(timer);
  }, []);

  const handleTouchStart = (e) => {
    startY.current = e.touches[0].clientY;
  };

  const handleTouchEnd = (e) => {
    if (!canSwipe) return;

    const endY = e.changedTouches[0].clientY;
    if (startY.current - endY > 80) {
      onSwipeUp();
    }
  };

  // Optional mouse support (desktop trackpad)
  const handleWheel = (e) => {
    if (!canSwipe) return;
    if (e.deltaY > 50) {
      onSwipeUp();
    }
  };

  return (
    <div
      className="landing"
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      onWheel={handleWheel}
    >
      {/* Star layers */}
      <div className="stars-layer1"></div>
      <div className="stars-layer2"></div>
      <div className="stars-layer3"></div>

      {/* Center zoom-in bot */}
      <div className="bot-wrapper">
        <img src={logo} alt="Bot" className="bot-zoom" />
      </div>

      {/* Optional hint (only after animation) */}
      {canSwipe && <div className="swipe-hint">Swipe up</div>}
    </div>
  );
}

export default LandingPage;