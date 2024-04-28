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

const Content = styled("div")(({ theme }) => ({
  margin: "10rem 3rem 3rem 3rem",
}));

const MissionStatement = styled("div")(({ theme }) => ({
  margin: "0 0 2rem 3rem",
  ".bold":{
    fontSize: '65px',
    justifyContent: 'center',
    margin: "0rem 2rem",
    width: '80vw',
    textAlign: "center"
  },
  ".normal":{
    fontSize: '20px',
    justifyContent: 'center',
    margin: "0rem 2rem",
    width: '80vw',
    textAlign: "center",
    fontWeight: 'normal'
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

// Styled component for the arrow
const Arrow = styled('div')`
  width: 0;
  height: 0;
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-top: 30px solid #333;
  margin: 0 auto;
  animation: ${bounceAnimation} 1s infinite;
  cursor: pointer;
`;

// Wrapper component to center the arrow
const Wrapper = styled('div')`
  justify-content: center;
  align-items: center;
  margin-bottom: 5rem;
`;

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
      <Content>
        <MissionStatement>
          <p className="bold">
            Empowering careers by connecting<br /> you with the latest innovations
          </p>
          <p className="normal">
            Discover your next opportunity with companies <br /> fuelled by venture capital at VC Hub.
          </p>
        </MissionStatement>
        <Wrapper>
          <ScrollLink to="table" spy={true} smooth={true} duration={500}>
            <Arrow onClick={scrollToTable} />
          </ScrollLink>
        </Wrapper>
        <div ref={tableRef}>
          <Table />
        </div>
      </Content>
    </ThemeProvider>
  );
};

export default Main;
