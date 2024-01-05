import { AppBar, Switch, styled } from "@mui/material";
import moon from "./../assets/moon.png";
import sun from "./../assets/sun.png";
import { Dispatch, FC, SetStateAction } from "react";

const HeaderWrapper = styled("div")(
  ({ theme }) => `
  color: ${theme.palette.primary.light};
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin:0 0;

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
}

const Header: FC<Props> = ({ setIsLightTheme }) => {
  const label = { inputProps: { "aria-label": "Toggle Dark Mode" } };
  return (
    <>
      <AppBar position="static">
        <HeaderWrapper>
          <h2>VC HUB</h2>
          <MaterialUISwitch
            {...label}
            className="toggle"
            onClick={() => {
              setIsLightTheme((prev) => !prev);
            }}
          />
        </HeaderWrapper>
      </AppBar>
    </>
  );
};

export default Header;
