import { Article, VCData } from "../Interfaces";

const getVCData = ()=>{

    const url = process.env.REACT_APP_VC_HUB_URL
    return fetch(url??"")
    .then(response => response.json())
    .then((res: Article[]) => {return res})
    .catch(error => {console.error(error); return [];});
}

export default getVCData;