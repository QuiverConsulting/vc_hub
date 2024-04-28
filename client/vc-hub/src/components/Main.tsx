import { ThemeProvider, createTheme, styled } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Table from "./table/Table";
import Header from "./Header";
import { useEffect, useState } from "react";
import background from '../assets/background.png';


const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: '#e3f2fd',
      contrastText: '#131111',
    },
    background:{
      default: '#0a0a0a'
    },
    text:{
      primary:'#e3f2fd',
      secondary: '#424242'
    }
  },
});

const lightTheme = createTheme({
  palette: {
    mode: "light",
    text:{
      secondary: '#d8e3ee'
    }
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundImage: `url(${background})`
      }
    }
  }
}
  
});

const Content = styled("div")(({ theme }) => ({
  margin: "3rem",
}));

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
      <Content>
        <Table />
      </Content>
    </ThemeProvider>
  );
};

export default Main;
