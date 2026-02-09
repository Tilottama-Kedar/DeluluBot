import "../App.css";
import logo from "../assets/logo.png";

function LandingPage() {
  return (
    <div className="landing">
      {/* Original top-left logo (unchanged) */}
      <img src={logo} alt="Logo" className="landing-logo" />

      {/* Center zoom-in bot */}
      <div className="bot-wrapper">
        <img src={logo} alt="Bot" className="bot-zoom" />
      </div>
    </div>
  );
}

export default LandingPage;