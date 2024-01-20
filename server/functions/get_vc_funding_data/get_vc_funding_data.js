import { MongoClient } from "mongodb";
import dotenv from "dotenv";

dotenv.config();

const handler = async (event) => {
  const client = new MongoClient(process.env.DB_CONNECTION_STR);
  let conn;
  try {
    conn = await client.connect();
  } catch (e) {
    return { statusCode: 500, body: e.toString() };
  }
  const db = conn.db(process.env.DB_NAME);
  const collection = await db.collection(process.env.DB_FUNDING_COLLECTION);
  const results = await collection
    .find({ company_name: { $ne: null } }, { _id: 0 })
    .sort({ date: -1 })
    .limit(parseInt(process.env.NUM_FUNDING_ENTRIES) || 1500)
    .toArray();

  return {
    statusCode: 200,
    body: JSON.stringify(results),
    headers: {
			'Content-Type': 'application/json; charset=utf-8'
		},
  };
};

module.exports = { handler };
