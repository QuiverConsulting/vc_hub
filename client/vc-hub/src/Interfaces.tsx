export interface Article {
  company_name: string | null;
  date: Date | null;
  link: string | null;
  currency: string | null;
  financiers: string[] | null;
  funding: number | null;
  location: string | null;
  series: string | null;
  timestamp: Date | null;
}

export interface VCData {
  articles: Article[];
  expiry_date: Date | null;
}
