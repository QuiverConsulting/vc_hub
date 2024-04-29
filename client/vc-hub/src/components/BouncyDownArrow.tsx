import styled, { keyframes } from "styled-components";
import downArrowImage from '../assets/arrow-down.png';


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

export const BouncyDownArrow  = styled('div')`
    width: 40px; 
    height: 40px; 
    background-image: url(${downArrowImage});
    background-size: cover;
    background-repeat: no-repeat;
    animation: ${bounceAnimation} 1s infinite;
    cursor: pointer;
`;