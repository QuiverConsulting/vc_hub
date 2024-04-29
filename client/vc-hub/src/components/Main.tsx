import { ThemeProvider, createTheme, styled } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Table from "./table/Table";
import Header from "./Header";
import { useEffect, useState, useRef } from "react";
import background from '../assets/background.png';
import { Link as ScrollLink } from 'react-scroll';
import { BouncyDownArrow } from "./BouncyDownArrow";

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

const TableWrapper = styled("div")(({ theme }) => ({
  margin: "10vh 5vw 5vh 5vw",
  height: '80vh',
  alignContent: 'center'
}));

const MissionStatementWrapper = styled("div")(({ theme }) => ({
  textAlign: 'center',
  ".bold":{
    fontSize: '65px'
  },
  ".normal":{
    fontSize: '20px'
  },
}));


const ArrowWrapper = styled('div')`
  position: absolute;
  bottom: 3vh;
  left: 50%;
  transform: translateX(-50%);
`;


const ContentWrapper = styled("div")(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  flexDirection: 'column',
  justifyContent: 'center',
  height: '95vh'

}));

const Main = () => {
  const localIsLightTheme = localStorage.getItem("isLightTheme")
  const [theme, setTheme] = useState(localIsLightTheme ===null || localIsLightTheme ==="true"?lightTheme:darkTheme );
  const [isLightTheme, setIsLightTheme] = useState<boolean>(localIsLightTheme ===null || localIsLightTheme ==="true"?true:false );
  const tableRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
      localStorage.setItem("isLightTheme", isLightTheme.toString())
      isLightTheme ? setTheme(lightTheme) : setTheme(darkTheme);
  }, [isLightTheme]);



  const scrollToTable = () => {
    if (tableRef.current) {
      tableRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header setIsLightTheme={setIsLightTheme} isLightTheme={isLightTheme}/>
     
        <ContentWrapper>
        <MissionStatementWrapper>
          <p className="bold">
            Empowering careers by connecting<br /> you with the latest innovations
          </p>
          <p className="normal">
            Discover your next opportunity with companies <br /> fuelled by venture capital at VC Hub.
          </p>
        </MissionStatementWrapper>
          <ScrollLink to="table" spy={true} smooth={true} duration={500} className="arrow">
            <ArrowWrapper>
            <BouncyDownArrow onClick={scrollToTable} />
            </ArrowWrapper>
          </ScrollLink>
        </ContentWrapper>
        <TableWrapper ref={tableRef}>
          <Table />
      </TableWrapper>
    </ThemeProvider>
  );
};

export default Main;
