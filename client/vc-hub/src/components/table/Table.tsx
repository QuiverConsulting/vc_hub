import { useEffect, useState } from "react";
import {
  MaterialReactTable,
  MRT_Row,
  useMaterialReactTable,
} from "material-react-table";
import getVCData from "../../apis/getVCData";
import { Article, VCData } from "../../Interfaces";
import tableColumns from "./TableColumns";
import styled from "styled-components";
import { LinearProgress } from "@mui/material";
import moment from "moment";

const ProgressWrapper = styled.div`
  text-align: center;
  margin: 20rem 40rem;
`;

const Table = () => {
  const [articles, setArticles] = useState<Article[] | undefined>(undefined);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const expiry = localStorage.getItem("expiryDate");

    if (expiry === null || (expiry !== null && moment(expiry).isBefore(moment()))) {
      getVCData()?.then((data)=> {
        localStorage.setItem('articles', JSON.stringify(data.articles));
        if (data.expiry_date)
          localStorage.setItem('expiryDate',  new Date(data.expiry_date).toISOString());
        setArticles(data.articles);
      });
    } else {
      const localArticles = localStorage.getItem("articles");
      if (localArticles) setArticles(JSON.parse(localArticles));
    }
    setIsLoading(false);
  }, []);

  const table = useMaterialReactTable({
    columns: tableColumns,
    data: articles ?? [],
    initialState: {
      density: "compact",
      pagination: { pageSize: 25, pageIndex: 0 },
      sorting: [{id: "date", desc:true}]
    },
    muiTableContainerProps: { sx: { maxHeight: "65vh" } },
    enableStickyHeader: true,
    enableColumnOrdering: true,
    enableRowPinning: true,
    enableRowNumbers: true,
    rowNumberDisplayMode: "original",
    enableRowOrdering: true,
    muiRowDragHandleProps: ({ table }) => ({
      onDragEnd: () => {
        const { draggingRow, hoveredRow } = table.getState();
        if (hoveredRow && draggingRow) {
          articles?.splice(
            (hoveredRow as MRT_Row<Article>).index,
            0,
            articles.splice(draggingRow.index, 1)[0]
          );
          if (articles) setArticles([...articles]);
        }
      },
    }),
  });

  return (
    <>
      {isLoading ? (
        <ProgressWrapper>
          <LinearProgress />
        </ProgressWrapper>
      ) : (
          <MaterialReactTable table={table} />
      )}
    </>
  );
};

export default Table;
