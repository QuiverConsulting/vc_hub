import { createTheme } from "@mui/material";
import background from './assets/background.png';

export const darkTheme = createTheme({
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
  
  export const lightTheme = createTheme({
    palette: {
      mode: "light",
      text:{
        secondary: '#d8e3ee'
      },
      secondary: {
        main: '#fdfaf9',
        dark: '#000000'

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
  