import { useState } from "react";
import LandingPage from "./pages/LandingPage";
import Home from "./pages/Home";

function App() {
  const [page, setPage] = useState("landing");

  return (
    <>
      {page === "landing" && <LandingPage onSwipeUp={() => setPage("home")} />}
      {page === "home" && <Home />}
    </>
  );
}

export default App;
