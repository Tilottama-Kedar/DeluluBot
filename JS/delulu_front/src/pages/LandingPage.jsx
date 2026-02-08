import "../App.css";
import logo from "../assets/logo.png";

function LandingPage() {
  return (
    <div className="landing">
      {/* Logo fixed at top-left */}
      <img src={logo} alt="DeluluBot Logo" className="landing-logo" />
    </div>
  );
}

export default LandingPage;
