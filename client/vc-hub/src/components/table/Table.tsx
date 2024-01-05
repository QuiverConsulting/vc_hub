import { useEffect, useState } from "react";
import {
  MaterialReactTable,
  MRT_Row,
  useMaterialReactTable,
} from "material-react-table";
import getVCData from "../../apis/getVCData";
import { Article } from "../../Interfaces";
import tableColumns from "./TableColumns";
import { LinearProgress, darken, styled } from "@mui/material";
import moment from "moment";

const ProgressWrapper = styled("div")(
  ({ theme }) => `
  text-align: center;
  margin: 20rem 40rem;
`
);

const DescriptionWrapper = styled("div")(
  ({ theme }) => `
  display:flex;
  flex-direction: row;
`
);

const Table = () => {
  const [articles, setArticles] = useState<Article[] | undefined>(undefined);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [expiryDate, setExpiryDate] = useState<string>("");

  useEffect(() => {
    (async () => {
      const expiry = localStorage.getItem("expiryDate");
      if (
        expiry === null ||
        (expiry !== null && moment(expiry).isBefore(moment()))
      ) {
        const data = await getVCData();
        if (data.expiry_date) {
          const expiryString = new Date(data.expiry_date).toISOString();
          localStorage.setItem("expiryDate", expiryString);
          setExpiryDate(expiryString);
        }
        const articlesSorted = data.articles?.sort((a, b) =>
          b.date && a.date && moment(a.date).isAfter(moment(b.date)) ? -1 : 1
        ).map((a)=>({...a, 'fundingString': a.currency && a.funding ? a.currency.concat(a.funding.toLocaleString()): ""}));
        localStorage.setItem("articles", JSON.stringify(articlesSorted));
        setArticles(articlesSorted);
      } else {
        const localArticles = localStorage.getItem("articles");
        if (localArticles) setArticles(JSON.parse(localArticles));
        setExpiryDate(expiry);
      }
      setIsLoading(false);
    })();
  }, []);

  const table = useMaterialReactTable({
    columns: tableColumns,
    data: articles ?? [],
    initialState: {
      density: "compact",
      pagination: { pageSize: 25, pageIndex: 0 },
    },
    muiTableContainerProps: { sx: { maxHeight: "63vh" } },
    enableStickyHeader: true,
    enableColumnOrdering: true,
    enableRowPinning: true,
    enableRowNumbers: true,
    rowNumberDisplayMode: "original",
    enableRowOrdering: true,
    enableFilterMatchHighlighting: true,
    muiTableBodyProps: {
      sx: (theme) => ({
     
        '& tr:nth-of-type(odd) > td': {
          backgroundColor: theme.palette.text.secondary,
        },
        '& tr:nth-of-type(odd):not([data-selected="true"]):not([data-pinned="true"]):hover > td': {
          backgroundColor: darken(theme.palette.text.secondary, 0.2),
        },
      }),
    },

    mrtTheme: (theme) => ({
      baseBackgroundColor: theme.palette.primary.contrastText,
    }),
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
        <>
          <DescriptionWrapper>
            <p>Daily updated list of VC funded companies.</p>
            {expiryDate && (
              <p>
                &nbsp;Last Updated on{" "}
                {moment(expiryDate)
                  .subtract(1, "days")
                  .local()
                  .format("dddd MMM DD YYYY")}
                .
              </p>
            )}
          </DescriptionWrapper>
          <MaterialReactTable table={table} />
        </>
      )}
    </>
  );
};

export default Table;
