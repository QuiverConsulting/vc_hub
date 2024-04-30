import { AppBar, Button, Switch, styled } from "@mui/material";
import moon from "./../assets/moon.png";
import sun from "./../assets/sun.png";
import { Dispatch, FC, SetStateAction, useEffect, useState } from "react";
import VCHLogo from '../assets/vch_logo.svg';
import { Link } from "react-router-dom";

const HeaderWrapper = styled("div")(
  ({ theme }) => `
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 0 4.4vw; 
  button{
    margin-right: 5rem;
  }
`
);

const MaterialUISwitch = styled(Switch)(({ theme }) => ({
  width: 62,
  height: 34,
  padding: 7,
  "& .MuiSwitch-switchBase": {
    margin: 1,
    padding: 0,
    transform: "translateX(6px)",
    "&.Mui-checked": {
      color: "#fff",
      transform: "translateX(22px)",
      "& .MuiSwitch-thumb:before": {
        backgroundImage: `url(${moon})`,
        backgroundSize: "20px 20px",
      },
      "& + .MuiSwitch-track": {
        opacity: 1,
        backgroundColor: theme.palette.grey[500],
      },
    },
  },
  "& .MuiSwitch-thumb": {
    backgroundColor: theme.palette.primary.light,
    width: 32,
    height: 32,
    "&::before": {
      content: "''",
      position: "absolute",
      width: "100%",
      height: "100%",
      left: 0,
      top: 0,
      backgroundRepeat: "no-repeat",
      backgroundPosition: "center",
      backgroundImage: `url(${sun})`,
      backgroundSize: "20px 20px",
    },
  },
  "& .MuiSwitch-track": {
    opacity: 1,
    backgroundColor: theme.palette.grey[200],
    borderRadius: 20 / 2,
  },
}));

interface Props {
  setIsLightTheme: Dispatch<SetStateAction<boolean>>;
  isLightTheme: boolean;
}

const Header: FC<Props> = ({ setIsLightTheme, isLightTheme}) => {
  const [isAtTop, setIsAtTop] = useState(true);

  const label = { inputProps: { "aria-label": "Toggle Dark Mode" } };

  useEffect(() => {
    const handleScroll = () => {
      const isTop = window.scrollY === 0;
      setIsAtTop(isTop);
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <>
      <AppBar position="fixed" elevation={0} color={isAtTop ? "transparent" : "secondary"} sx = {{  height:'10vh',  justifyContent:'center' } }>
        <HeaderWrapper>
        <Link to="/"> 
        <img src={VCHLogo} alt="VCH Logo" width="120"  />
        </Link>
          {/* <MaterialUISwitch
            {...label}
            className="right"
            defaultChecked={!isLightTheme}
            onClick={() => {
              setIsLightTheme((prev) => !prev);
            }}
          /> */}
          {/* <div>
            <Link to="/about"> 
              <Button variant="text" >About</Button>
            </Link>
            <Button variant="contained" sx={{backgroundColor: 'common.black' }} >Buy us coffee</Button>
          </div> */}
        </HeaderWrapper>
      </AppBar>
    </>
  );
};

export default Header;
