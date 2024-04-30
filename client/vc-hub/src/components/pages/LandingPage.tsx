
import Table from "../table/Table";
import { useRef } from "react";
import { Link as ScrollLink } from 'react-scroll';
import { BouncyDownArrow } from "../BouncyDownArrow";
import styled from "styled-components";



const TableWrapper = styled("div")(({ theme }) => ({
  margin: "10vh 5vw 5vh 5vw",
  height: '90vh',
  alignContent: 'center'
}));

const MissionStatementWrapper = styled("div")(({ theme }) => ({
  textAlign: 'center',
  ".bold":{
    fontSize: 'calc(3vw + 10px)'
  },
  ".normal":{
    fontSize: 'calc(1vw + 7px)'
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

const LandingPage = () => {

  const tableRef = useRef<HTMLDivElement>(null);
  const scrollToTable = () => {
    if (tableRef.current) {
      tableRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <>
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
    </TableWrapper></>
  );
};

export default LandingPage;
