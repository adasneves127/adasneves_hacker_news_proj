import {Database} from 'sqlite3'


class databaseConnection{

    private db: any

    constructor(dbName: string) {
        this.db = new Database(dbName, (err) => {
            if(err) console.log(err)
        })
    }

    createTable(dbName: string){

    }

}


if(require.main == module){

}