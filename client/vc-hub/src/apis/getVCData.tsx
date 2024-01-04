import { VCData } from "../Interfaces";

function timeout(delay: number) {
    return new Promise( res => setTimeout(res, delay) );
}


async function fetchWithRetries(url: string, retriesNum = 5, delayMilli = 3000, retryErrorCodes: number[]) {
    let currentRetry = 0;
    while (currentRetry < retriesNum) {

        const response = await fetch(url);
        if (response.ok) 
        {
          return await response.json();
        }
        else if (retryErrorCodes.includes(response.status)) 
        {
          currentRetry++;
          console.log(`${url} responded with ${response.status}, retrying in ${delayMilli/1000} seconds. Retrying ${currentRetry} out of ${retriesNum} trys.`);
          await timeout(delayMilli);
        } 
        else 
        {
            console.error(`Unable to get data from ${url}, responded with ${response.status}.`);
            return null
        }
    }
    console.error(`Unable to get data from ${url}, retried ${retriesNum} times.`);
    return null
  }

  async function getVCData() {
    console.log("getting data...");
    const url = process.env.REACT_APP_VC_HUB_URL
    const retriesNum = process.env.REACT_APP_API_MAX_RETRIES_NUM ? parseInt(process.env.REACT_APP_API_MAX_RETRIES_NUM): 5
    const delay = process.env.REACT_APP_API_RETRY_DELAY_MILLI ? parseInt(process.env.REACT_APP_API_RETRY_DELAY_MILLI): 3000
    const dataRaw: VCData | null = await fetchWithRetries(url??"", retriesNum, delay, [404])
    let data: VCData = {articles:[], expiry_date: null}
    if (dataRaw)
    {
     data = {...dataRaw}
    }  
    return data 
}

export default getVCData;