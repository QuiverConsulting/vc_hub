import styled from "styled-components";
import Table from "./table/Table";

const Header = styled.h1`
  color: blue;
  text-align: center;
`;

const Content = styled.div`
  margin: 3rem;
`;
const Main = () => {
  return (
    <>
      <Header>VC HUB</Header>
      <Content>
        <p>Daily updated list of VC funded companies.</p>
        <Table />
      </Content>
    </>
  );
};

export default Main;
