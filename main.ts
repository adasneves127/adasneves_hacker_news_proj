import { getData } from "./webGet"
import {entry, Response} from "./Utils"
import 'fs'
import * as fs from "fs";

const outputFile: fs.WriteStream = fs.createWriteStream('output.txt', )

const articles: Array<entry> = []

async function fetch_all_pages(){
    let total_pages = 0;
    let page_count = 0
    do {
        const data: Response =
            await getData(`http://hn.algolia.com/api/v1/search?query=Ask HN: Who is hiring%3F&page=${page_count}`) as Response
        if(total_pages == 0) {
            total_pages = data.nbPages
        }
        getKeyData(data)
        page_count++;
    } while(page_count <= total_pages)
}


function isWithinYear(article: entry){
    const articleDate = new Date(article.created_at);
    const currentDate = new Date()

    // If the current year is equal to the year that the article was published, then it is automatically valid.
    if(currentDate.getFullYear() == articleDate.getFullYear()){
        return true
    } else if (currentDate.getFullYear()-1 == articleDate.getFullYear()){
        // Otherwise, if the article year is one less than the current year:

        // And the article was published later than the current month, then it is valid.
        if(articleDate.getMonth() > currentDate.getMonth())
            return true
    }


}

function isCorrectArticleType(article: entry){
    return article.title.startsWith("Ask HN: Who is hiring?")
}

function getKeyData(current_page: Response){
    current_page.hits.forEach(article => {
        if(typeof article.title === "string" && isCorrectArticleType(article) && isWithinYear(article))
            articles.push(article)
    })
}



function writeToFile(){
    articles.forEach(article => {
        const title_split = article.title.split('(')
        const date = title_split[1].slice(0, title_split[1].length - 1)


        outputFile.write(`${date}, ${article.num_comments}\n`)
    })
}

async function main (){
    outputFile.write("Date, Top-Level-Comments\n")

    await fetch_all_pages()

    writeToFile()
    outputFile.close()
}

// Equivalent of Python's 'if __name__ == "__main__":'
if (require.main === module) {
    main()
}
