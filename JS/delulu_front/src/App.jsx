import { useEffect, useRef, useState } from "react";
import LandingPage from "./pages/LandingPage";
import Home from "./pages/Home";

function App() {
  const [page, setPage] = useState("landing");

  // 🔽 Added refs & effect ONLY (no JSX changes)
  const startY = useRef(0);

  useEffect(() => {
    if (page !== "home") return;

    const handleTouchStart = (e) => {
      startY.current = e.touches[0].clientY;
    };

    const handleTouchEnd = (e) => {
      const endY = e.changedTouches[0].clientY;

      // swipe DOWN → back to landing
      if (endY - startY.current > 80) {
        setPage("landing");
      }
    };

    const handleWheel = (e) => {
      // trackpad / mouse scroll UP
      if (e.deltaY < -50) {
        setPage("landing");
      }
    };

    window.addEventListener("touchstart", handleTouchStart);
    window.addEventListener("touchend", handleTouchEnd);
    window.addEventListener("wheel", handleWheel);

    return () => {
      window.removeEventListener("touchstart", handleTouchStart);
      window.removeEventListener("touchend", handleTouchEnd);
      window.removeEventListener("wheel", handleWheel);
    };
  }, [page]);

  return (
    <>
      {page === "landing" && <LandingPage onSwipeUp={() => setPage("home")} />}
      {page === "home" && <Home />}
    </>
  );
}

export default App;
