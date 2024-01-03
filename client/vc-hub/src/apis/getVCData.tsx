import { VCData } from "../Interfaces";

function timeout(delay: number) {
    return new Promise( res => setTimeout(res, delay) );
}

function getVCData(retries = 5): Promise<VCData> {
    console.log("getting data...");
    const url = process.env.REACT_APP_VC_HUB_URL
    return fetch(url??"")
        .then(async function(response) {
            if (response.ok) {
                return response.json();
            }
            console.log("Failed to get data, waiting for 3 seconds before retry.");
            await timeout(3000); //for 3 sec delay
            throw new Error("HTTP status " + response.status)
        })
        .then((res: VCData) => {return res})
        .catch(error => {
            if (retries <= 0) {
                console.error(error) 
                return [] as unknown as VCData
            }
            return getVCData(retries - 1);
        });
    }

export default getVCData;