import { ThemeProvider, createTheme, styled } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Table from "./table/Table";
import Header from "./Header";
import { useEffect, useState } from "react";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: '#e3f2fd',
      contrastText: '#131111',
    },
    background:{
      default: '#0a0a0a'
    }
  },
});

const lightTheme = createTheme({
  palette: {
    mode: "light",
  },
});

const Content = styled("div")(({ theme }) => ({
  margin: "3rem",
}));

const Main = () => {
  const [theme, setTheme] = useState(lightTheme);
  const [isLightTheme, setIsLightTheme] = useState(true);

  useEffect(() => {
    isLightTheme ? setTheme(lightTheme) : setTheme(darkTheme);
  }, [isLightTheme]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header setIsLightTheme={setIsLightTheme} />
      <Content>
        <Table />
      </Content>
    </ThemeProvider>
  );
};

export default Main;
