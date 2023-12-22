import { MRT_ColumnDef } from "material-react-table";
import { Article } from "../../Interfaces";

const tableColumns: MRT_ColumnDef<Article>[] = [
  {
    accessorKey: "company_name",
    header: "Company Name",
    size: 150,
  },
  {
    accessorKey: "funding",
    header: "Funding",
    size: 100,
  },
  {
    accessorKey: "currency",
    header: "Currency",
    size: 50,
  },
  {
    accessorKey: "location",
    header: "Location",
    size: 150,
  },

  {
    accessorFn: (row) => row.financiers?.toString(),
    header: "Financiers",
    size: 100,
  },

  {
    accessorKey: "series",
    header: "Series",
    size: 100,
  },
  {
    accessorKey: "date",
    header: "Date",
    size: 100,
  },
  {
    accessorKey: "link",
    header: "Link",
    size: 150,
  },
];

export default tableColumns;
