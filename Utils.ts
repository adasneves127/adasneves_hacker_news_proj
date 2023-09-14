
export interface entry {
    created_at: string,
    title: string | null,
    num_comments: number
}

export interface Response {
    hits: Array<entry>,
    nbHits: number,
    page: number,
    nbPages: number
    hitsPerPage: 20,
    exhaustiveNbHits: boolean,
    exhaustiveType: boolean
    exhaustive: {nbHits: boolean, typo: boolean},
    query: string,
    params: string,
    processingTimeMS: number,
    processingTimingsMS: {
        _request: { roundTrip: number },
        afterFetch: { format: object, total: number },
        fetch: { query: number, scanning: number, total: number },
        total: number
    },
    serverTimeMS: number

}