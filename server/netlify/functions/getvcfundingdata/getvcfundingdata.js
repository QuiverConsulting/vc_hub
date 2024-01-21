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
  let collection = db.collection(process.env.DB_FUNDING_COLLECTION);
  const results = await collection
    .find({ company_name: { $ne: null } }, { _id: 0 })
    .sort({ date: -1 })
    .limit(parseInt(process.env.NUM_FUNDING_ENTRIES) || 1500)
    .toArray();

    collection = db.collection(process.env.DB_EXPIRY_DATE_COLLECTION);
    const expiry_date = await collection.findOne({"title": "expiry_date"}, {'_id': 0})
    const entries = {'articles': results, 'expiry_date': expiry_date.expiry_date}

    client.close()

  return {
    statusCode: 200,
    body: JSON.stringify(entries),
    headers: {
			'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*'
		},
  };
};

module.exports = { handler };
