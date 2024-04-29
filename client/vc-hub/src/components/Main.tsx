import { ThemeProvider, createTheme, keyframes, styled } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Table from "./table/Table";
import Header from "./Header";
import { useEffect, useState, useRef } from "react";
import background from '../assets/background.png';
import { Link as ScrollLink } from 'react-scroll';

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
  margin: "10vh 5vw",
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

// Keyframe animation for bouncing
const bounceAnimation = keyframes`
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(8px);
  }
  100% {
    transform: translateY(0);
  }
`;

const Arrow = styled('div')`
  position: absolute;
  bottom: 3vh;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-top: 30px solid #333;
  animation: ${bounceAnimation} 1s infinite;
  cursor: pointer;
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
            <Arrow onClick={scrollToTable} />
          </ScrollLink>
        </ContentWrapper>
        <TableWrapper ref={tableRef}>
          <Table />
      </TableWrapper>
    </ThemeProvider>
  );
};

export default Main;
