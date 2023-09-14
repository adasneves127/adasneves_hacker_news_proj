import fetch from 'node-fetch';
import {WebResponse} from "./Utils"


export async function getData(url: string): Promise<WebResponse> {
    return fetch(url).then((res) => { return res.json() as unknown as WebResponse});
}