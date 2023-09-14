import { getData } from "./webGet"
import {entry, WebResponse} from "./Utils"
import 'fs'
import * as fs from "fs";

// Global variables
const outputFile: fs.WriteStream = fs.createWriteStream('output.txt') // Text stream for writing output file
const articles: Array<entry> = [] // List of valid articles

/**
 * Get all pages from Algolia, where query is 'Ask HN: Who is hiring?'
 * @return Promise<void> Returns a promise to be resolved when request is fulfilled
 */
async function fetch_all_pages(){
    // Keep track of the total pages of data, and the page we are on.
    let total_pages = 0;
    let page_count = 0

    // We need to do 1 page of searching no matter what
    do {
        // Get the data from the website.
        const data: WebResponse = // We cast to 'Unknown' to avoid type conversion issues, then we convert to an interface 'Response'
            await getData(`http://hn.algolia.com/api/v1/search?query=Ask HN: Who is hiring%3F&page=${page_count}`)

        // If this is the first page, update the total pages to what the request told us.
        if(total_pages == 0) {
            total_pages = data.nbPages
        }
        // Capture only the results from the request that matter to us.
        getKeyData(data)

        // Increment the page count
        page_count++;
    } while(page_count <= total_pages) // Repeat until our page count is G.T. our total pages.
}

/**
 *  Check to see if the date the article was published was within the past 12 months.
 * @param article The article to check against
 * @returns Boolean Is the data within the current year
 */
export function isWithinYear(article: entry){
    // Convert the date the article was created at to a 'Date' object
    const articleDate = new Date(article.created_at);
    // Get the current datetime from the system
    const currentDate = new Date()

    // If the current year is equal to the year that the article was published, then it is automatically valid.
    if(currentDate.getFullYear() == articleDate.getFullYear()){
        return true
    }

    // If the article year is one less than the current year:
    if (currentDate.getFullYear()-1 == articleDate.getFullYear()){

        // And the article was published later than the current month, then it is valid.
        if(articleDate.getMonth() > currentDate.getMonth())
            return true
    }

    //Else, return false.
    return false
}

/**
 *
 * @param article
 */
export function isCorrectArticleType(article: entry){
    if(typeof article.title !== "string") return false
    return article.title.startsWith("Ask HN: Who is hiring?")
}

function getKeyData(current_page: WebResponse){
    current_page.hits.forEach(article => {
        if(typeof article.title === "string" && isCorrectArticleType(article) && isWithinYear(article))
            articles.push(article)
    })
}



function writeToFile(){
    articles.forEach(article => {
        if(typeof article.title !== "string") return;

        const title_split = article.title.split('(')
        const date = title_split[1].slice(0, title_split[1].length - 1)

        outputFile.write(`${date}, ${article.num_comments}\n`)

    })
}

export function main (){
    outputFile.write("Date, Top-Level-Comments\n")

    //
    fetch_all_pages()
    writeToFile()
    outputFile.close()
}

// Equivalent of Python's 'if __name__ == "__main__":'
if (require.main === module) {
    main()
}
