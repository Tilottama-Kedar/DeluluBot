import "../App.css";
import logo from "../assets/logo.png";

function LandingPage() {
  return (
    <div className="landing">
      {/* Original top-left logo */}
      <img src={logo} alt="Logo" className="landing-logo" />

      {/* Star layers for twinkling galaxy */}
      <div className="stars-layer1"></div>
      <div className="stars-layer2"></div>
      <div className="stars-layer3"></div>

      {/* Center zoom-in bot */}
      <div className="bot-wrapper">
        <img src={logo} alt="Bot" className="bot-zoom" />
      </div>
    </div>
  );
}

export default LandingPage;
