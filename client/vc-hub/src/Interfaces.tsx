export interface Article {
  company_name: string | null;
  date: string | null;
  link: string | null;
  currency: string | null;
  financiers: string[] | null;
  funding: number | null;
  location: string | null;
  series: string | null;
  timestamp: Date | string | null;
}

export interface VCData {
  articles: Article[];
  expiryDate: Date | string;
}
