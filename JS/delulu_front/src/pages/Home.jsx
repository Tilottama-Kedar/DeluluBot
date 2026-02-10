import { useEffect, useState } from "react";

function Home() {
  // 🔒 Lock scroll
  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  // ⏱ Live Time & Date
  const [time, setTime] = useState("");
  const [date, setDate] = useState("");

  useEffect(() => {
    const updateClock = () => {
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

    updateClock();
    const interval = setInterval(updateClock, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        overflow: "hidden",
        background: `
          radial-gradient(
            circle,
            #e0b3ff 0%,
            #8a2be2 35%,
            #0d0018 100%
          )
        `,
        color: "white",
        fontFamily: "Inter, system-ui, sans-serif",
        padding: "32px",
        boxSizing: "border-box",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Top Bar */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "36px",
          opacity: 0.85,
        }}
      >
        <div>
          <div style={{ fontSize: "20px", letterSpacing: "2px", opacity: 0.7 }}>
            NEWSNEST
          </div>
          <div style={{ fontSize: "12px", opacity: 0.5 }}>
            NEST ACTIVE
          </div>
        </div>

        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: "18px", fontWeight: 600 }}>{time}</div>
          <div style={{ fontSize: "12px", opacity: 0.6 }}>{date}</div>
        </div>
      </div>

      {/* Main Content */}
      <div
        style={{
          display: "flex",
          flex: 1,
          gap: "48px",
        }}
      >
        {/* LEFT STACK (like sidebar but minimal) */}
        <div
          style={{
            width: "280px",
            display: "flex",
            flexDirection: "column",
            gap: "16px",
          }}
        >
          {[
            { title: "Daily Intel", desc: "Curated defence updates" },
            { title: "Mission Log", desc: "Track your learning streak" },
            { title: "Intel Feed", desc: "Live updates incoming" },
          ].map((item) => (
            <div
              key={item.title}
              style={{
                background: "rgba(255, 255, 255, 0.08)",
                borderRadius: "16px",
                padding: "18px",
                backdropFilter: "blur(14px)",
                border: "1px solid rgba(255,255,255,0.12)",
                cursor: "pointer",
              }}
            >
              <h3 style={{ marginBottom: "6px", fontWeight: 500 }}>
                {item.title}
              </h3>
              <p style={{ fontSize: "14px", opacity: 0.65 }}>
                {item.desc}
              </p>
            </div>
          ))}
        </div>

        {/* RIGHT CONTENT (unchanged placeholder) */}
        <div
          style={{
            flex: 1,
            borderRadius: "22px",
            background: "rgba(255,255,255,0.05)",
            border: "1px dashed rgba(255,255,255,0.18)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            opacity: 0.5,
          }}
        >
          Future intelligence modules will appear here
        </div>
      </div>
    </div>
  );
}

export default Home;
