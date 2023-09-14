import fetch from 'node-fetch';

export async function getData(url: string) {
    return await fetch(url);
}