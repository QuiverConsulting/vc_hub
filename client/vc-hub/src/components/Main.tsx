import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Header from "./Header";
import { useEffect, useState } from "react";
import { lightTheme, darkTheme } from "../Themes";
import LandingPage from "./LandingPage";


const Main = () => {
  const localIsLightTheme = localStorage.getItem("isLightTheme")
  const [theme, setTheme] = useState(localIsLightTheme ===null || localIsLightTheme ==="true"?lightTheme:darkTheme );
  const [isLightTheme, setIsLightTheme] = useState<boolean>(localIsLightTheme ===null || localIsLightTheme ==="true"?true:false );

  useEffect(() => {
      localStorage.setItem("isLightTheme", isLightTheme.toString())
      isLightTheme ? setTheme(lightTheme) : setTheme(darkTheme);
  }, [isLightTheme]);


  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header setIsLightTheme={setIsLightTheme} isLightTheme={isLightTheme}/>
      <LandingPage />
    </ThemeProvider>
  );
};

export default Main;
