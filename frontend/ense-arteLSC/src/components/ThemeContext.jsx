// ThemeContext.jsx
import { createContext, useContext, useState } from "react";

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState({
    backgroundColor: "#ffffff",
    textColor: "#000000",
    buttonColor: "#2241A0",
    textButtonColor: "#ffffff",
    secondaryButtonColor: "#ffffff",
    secondaryTextButtonColor: "#2241A0",
    auxcolor:"#b9e185",
  });

  const lightTheme = {
    backgroundColor: "#ffffff",
    textColor: "#000000",
    buttonColor: "#2241A0",
    textButtonColor: "#ffffff",
    secondaryButtonColor: "#ffffff",
    secondaryTextButtonColor: "#2241A0",
    auxcolor:"#b9e185",
  };
  
  const darkTheme = {
    backgroundColor: "#202f60",
    textColor: "#ffffff",
    buttonColor: "#B9E185",
    textButtonColor: "#263972",
    secondaryButtonColor: "transparent",
    secondaryTextButtonColor: "#ffffff",
    auxcolor:"#b9e185",
  };
  
  const toggleTheme = () => {
    setTheme((prevTheme) =>
      prevTheme.backgroundColor === lightTheme.backgroundColor ? darkTheme : lightTheme
    );
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
