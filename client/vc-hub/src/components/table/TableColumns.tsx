import { MRT_ColumnDef } from "material-react-table";
import { Article } from "../../Interfaces";
import moment from "moment";

const tableColumns: MRT_ColumnDef<Article>[] = [
  {
    accessorKey: "company_name",
    header: "Company Name",
    size: 150,
  },
  {
    accessorKey: "fundingString",
    header: "Funding",
    sortingFn: (rowA:any, rowB:any,columnId:any) =>{
      const a = parseInt(rowA.getValue(columnId).substring(1).replace(/,/g, '').replace(",","") , 10)
      const b = parseInt(rowB.getValue(columnId).substring(1).replace(/,/g, '').replace(",","") , 10) 
      return  (!Number.isNaN(a) ? a : -Infinity) - (!Number.isNaN(b) ? b : -Infinity)
    },
    size: 100
  },
  {
    accessorKey: "location",
    header: "Location",
    filterVariant: 'multi-select',
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
    Cell: ({ cell }) => moment(cell.getValue<Date>()).format('MMMM DD, YYYY'), 
    sortingFn: 'datetime',
    header: "Date",
    size: 100,
  },
  {
    accessorKey: "link",
    header: "Link",
    size: 150,
    Cell: ({ cell }) => <a href={cell.getValue<string>()} target="_blank" rel="noopener noreferrer" style={{color:'#007A53'}}>{cell.getValue<string>().slice(0,40).concat("...")}</a>
  },
];

export default tableColumns;
