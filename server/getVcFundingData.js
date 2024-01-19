import express, { Router } from "express";
import serverless from "serverless-http";
import { MongoClient } from "mongodb";
import dotenv from "dotenv";

dotenv.config();
const client = new MongoClient(process.env.DB_CONNECTION_STR);
let conn;
try {
  conn = await client.connect();
} catch(e) {
  console.error(e);
}
let db = conn.db(process.env.DB_NAME);


const api = express();
const router = Router();
router.get("/vc_funding_data", async (req, res) =>
{
    let collection = await db.collection(process.env.DB_FUNDING_COLLECTION);
    let results = await collection.find({"company_name": {"$ne": null}},{"_id":0})
    .sort({ "date": -1})
    .limit(parseInt(process.env.NUM_FUNDING_ENTRIES) || 1500)
    .toArray();
  res.send(results).status(200);
} );

api.use("/api/", router);

// const port = 8000
// api.listen(port, () => {
//     console.log(`Example app listening on port ${port}`)
//   })

export const handler = serverless(api);