import { useEffect, useState } from "react";

function Home() {
  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => (document.body.style.overflow = "auto");
  }, []);

  const [time, setTime] = useState("");
  const [date, setDate] = useState("");

  useEffect(() => {
    const tick = () => {
      const now = new Date();
      setTime(
        now.toLocaleTimeString("en-GB", {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
      setDate(
        now.toLocaleDateString("en-GB", {
          weekday: "long",
          day: "2-digit",
          month: "long",
          year: "numeric",
        })
      );
    };
    tick();
    const i = setInterval(tick, 1000);
    return () => clearInterval(i);
  }, []);

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showAuthPopup, setShowAuthPopup] = useState(false);
  const [authView, setAuthView] = useState("choice");
  const [activePanel, setActivePanel] = useState(null);
  const [pendingPanel, setPendingPanel] = useState(null);

  const [registerData, setRegisterData] = useState({
    password: "",
    confirmPassword: "",
  });

  const passwordsMatch =
    registerData.password &&
    registerData.password === registerData.confirmPassword;

  const handleLeftClick = (panel) => {
    if (!isLoggedIn) {
      setPendingPanel(panel);
      setShowAuthPopup(true);
      setAuthView("choice");
    } else {
      setActivePanel(panel);
    }
  };

  const handleLogin = () => {
    setIsLoggedIn(true);
    setShowAuthPopup(false);
    setActivePanel(pendingPanel);
    setPendingPanel(null);
  };

  const renderRightPanel = () => {
    if (!isLoggedIn) return "Login to access intelligence modules";
    if (activePanel === "daily") return "🛰 Daily Intel content appears here";
    if (activePanel === "mission") return "📊 Mission Log & streaks appear here";
    if (activePanel === "feed") return "📡 Live Intel Feed appears here";
    return "Select a module from the left";
  };

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        background:
          "radial-gradient(circle,#e0b3ff 0%,#8a2be2 35%,#0d0018 100%)",
        color: "white",
        padding: "32px",
        display: "flex",
        flexDirection: "column",
        boxSizing: "border-box",
      }}
    >
      {/* TOP BAR */}
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "36px" }}>
        <div>
          <div style={{ fontSize: "20px", letterSpacing: "2px", opacity: 0.7 }}>
            NEWSNEST
          </div>
          <div style={{ fontSize: "12px", opacity: 0.5 }}>NEST ACTIVE</div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: "18px", fontWeight: 600 }}>{time}</div>
          <div style={{ fontSize: "12px", opacity: 0.6 }}>{date}</div>
        </div>
      </div>

      {/* MAIN */}
      <div style={{ display: "flex", flex: 1, gap: "48px" }}>
        <div style={{ width: "280px", display: "flex", flexDirection: "column", gap: "16px" }}>
          <Panel
  title="Morning Nest"
  desc="Today’s defence news + GK briefing"
  onClick={() => handleLeftClick("brief")}
/>

<Panel
  title="Nest Drill"
  desc="Daily MCQ practice from today’s news"
  onClick={() => handleLeftClick("quiz")}
/>

<Panel
  title="Nest Archive"
  desc="Browse saved news & monthly records"
  onClick={() => handleLeftClick("archive")}
/>

        </div>

        <div
          style={{
            flex: 1,
            borderRadius: "22px",
            background: "rgba(255,255,255,0.05)",
            border: "1px dashed rgba(255,255,255,0.18)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            opacity: isLoggedIn ? 1 : 0.5,
          }}
        >
          {renderRightPanel()}
        </div>
      </div>

      {/* POPUP */}
      {showAuthPopup && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(0,0,0,0.55)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              width: "360px",
              padding: "40px 24px 26px",
              borderRadius: "22px",
              background:
                "linear-gradient(135deg, rgba(180,120,255,0.25), rgba(90,20,160,0.18))",
              backdropFilter: "blur(26px) saturate(160%)",
              WebkitBackdropFilter: "blur(26px) saturate(160%)",
              border: "1px solid rgba(255,255,255,0.22)",
              boxShadow:
                "0 12px 40px rgba(138,43,226,0.35), inset 0 0 20px rgba(255,255,255,0.08)",
              position: "relative",
            }}
          >
            {authView !== "choice" && (
              <div
                onClick={() => setAuthView("choice")}
                style={{
                  position: "absolute",
                  top: "10px",
                  left: "10px",
                  fontSize: "22px",
                  fontWeight: 700,
                  cursor: "pointer",
                  opacity: 0.85,
                }}
              >
                ←
              </div>
            )}

            {authView === "choice" && (
              <>
                <h3 style={{ marginBottom: "28px", textAlign: "center" }}>
                  Access Required
                </h3>
                <button style={btnStyle} onClick={() => setAuthView("login")}>
                  Login
                </button>
                <button style={btnStyle} onClick={() => setAuthView("register")}>
                  Register
                </button>
              </>
            )}

            {authView === "login" && (
              <>
                <h3 style={{ marginBottom: "22px", paddingLeft: "20px" }}>
                  Login
                </h3>
                <input style={inputStyle} placeholder="Email or Phone" />
                <input style={inputStyle} type="password" placeholder="Password" />
                <button style={btnStyle} onClick={handleLogin}>
                  Submit
                </button>
              </>
            )}

            {authView === "register" && (
              <>
                <h3 style={{ marginBottom: "22px", paddingLeft: "20px" }}>
                  Register
                </h3>
                <input style={inputStyle} placeholder="Email" />
                <input style={inputStyle} placeholder="Phone" />
                <input
                  style={inputStyle}
                  type="password"
                  placeholder="New Password"
                  onChange={(e) =>
                    setRegisterData({ ...registerData, password: e.target.value })
                  }
                />
                <input
                  style={inputStyle}
                  type="password"
                  placeholder="Confirm Password"
                  onChange={(e) =>
                    setRegisterData({
                      ...registerData,
                      confirmPassword: e.target.value,
                    })
                  }
                />
                <button
                  style={{ ...btnStyle, opacity: passwordsMatch ? 1 : 0.4 }}
                  disabled={!passwordsMatch}
                  onClick={() => setAuthView("login")}
                >
                  Submit
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

const Panel = ({ title, desc, onClick }) => (
  <div
    onClick={onClick}
    style={{
      background: "rgba(255,255,255,0.08)",
      borderRadius: "16px",
      padding: "18px",
      backdropFilter: "blur(14px)",
      border: "1px solid rgba(255,255,255,0.12)",
      cursor: "pointer",
    }}
  >
    <h3 style={{ marginBottom: "6px", fontWeight: 500 }}>{title}</h3>
    <p style={{ fontSize: "14px", opacity: 0.65 }}>{desc}</p>
  </div>
);

const inputStyle = {
  width: "100%",
  padding: "10px",
  marginBottom: "12px",
  borderRadius: "10px",
  border: "none",
};

const btnStyle = {
  width: "100%",
  padding: "12px",
  borderRadius: "12px",
  background: "#8a2be2",
  border: "none",
  color: "white",
  cursor: "pointer",
  marginBottom: "10px",
};

export default Home;
