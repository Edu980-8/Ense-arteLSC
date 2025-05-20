"use client";

import { motion } from "motion/react";
import { useState } from "react";
import { useTheme } from "./ThemeContext.jsx";

export default function LayoutAnimation() {
  const [isOn, setIsOn] = useState(false);
  const { toggleTheme } = useTheme();
  const { theme } = useTheme();
  const handleClick = () => {
    setIsOn(!isOn);
    toggleTheme();
  };

  return (
    <div className="flex flex-row items-center justify-center gap-2 ">
      <box-icon name='sun' color={theme.backgroundColor === "#ffffff" ? "#2241A0" : "#fff"} ></box-icon>
      <button
        style={{
          ...container,
          justifyContent: isOn ? "flex-end" : "flex-start",
        }}
        onClick={handleClick}
      >
        <motion.div
          key={isOn ? "on" : "off"} // ⚠️ importante: fuerza re-render y reanimación
          animate={{
            scale: [1, 1.1, 0.9, 1], // efecto rebote
          }}
          transition={{
            duration: 0.4,
            easing: "ease-out",
          }}
          style={handle}
        />
      </button>
      <box-icon name='moon' color={theme.backgroundColor === "#ffffff" ? "#2241A0" : "#fff"} ></box-icon>
    </div>
  );
}

const container = {
  width: 45,
  height: 30,
  backgroundColor: "#2241A0",
  borderRadius: 50,
  cursor: "pointer",
  display: "flex",
  padding: 5,
  transition: "justify-content 0.3s ease-in-out",
};

const handle = {
  width: 20,
  height: 20,
  backgroundColor: "#fff",
  borderRadius: "50%",
};
