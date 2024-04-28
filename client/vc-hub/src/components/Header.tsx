import { AppBar, Switch, styled } from "@mui/material";
import moon from "./../assets/moon.png";
import sun from "./../assets/sun.png";
import { Dispatch, FC, SetStateAction } from "react";
import VCHLogo from '../assets/vch_logo.svg';

const HeaderWrapper = styled("div")(
  ({ theme }) => `
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: left;
  margin-left: 35px;

  .toggle{
    right: 0;
    position: absolute;
    margin-right:2rem;
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
  const label = { inputProps: { "aria-label": "Toggle Dark Mode" } };
  return (
    <>
      <AppBar position="fixed" elevation={0} sx = {{ background: '#fdfaf9' }}>
        <HeaderWrapper>
        <img src={VCHLogo} alt="VCH Logo" width="120" height="100"  style={{opacity:'100!important'}}/>
          {/* <MaterialUISwitch
            {...label}
            className="toggle"
            defaultChecked={!isLightTheme}
            onClick={() => {
              setIsLightTheme((prev) => !prev);
            }}
          /> */}
        </HeaderWrapper>
      </AppBar>
    </>
  );
};

export default Header;
