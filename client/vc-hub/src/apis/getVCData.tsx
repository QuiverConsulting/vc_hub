import { VCData } from "../Interfaces";

const getVCData = ()=>{

    console.log("getting data...");
    const url = process.env.REACT_APP_VC_HUB_URL
    return fetch(url??"")
    .then(response => response.json())
    .then((res: VCData) => {return res})
    .catch(error => {console.error(error); return [] as unknown as VCData;});
}

export default getVCData;