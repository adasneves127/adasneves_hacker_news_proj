import test from 'node:test';
import {getData} from "./webGet";
import assert from "assert";
import {entry} from './Utils'
import {isWithinYear, isCorrectArticleType} from './main'

test("Ensure web data is not corrupted", async () => {
    // Get a response from a test site, return the object as an object upon resolution of the promise
    const reply = await getData("https://adasneves.info/test.json").then(
        (res ) => {return res as object}
    )

    // Ensure that all the data is the same.
    assert.deepStrictEqual(reply, { message: 'Test Information!' })
})


test("Date comparison is correct",
    () => {
        // Current date and time
        const testEntry_now: entry = {
            title: 'This is a fake article!',
            created_at: `${new Date()}`,
            num_comments: -1
        }

        // 1 hour before
        const testEntryHourBefore: entry = {
            title: 'This is a fake article as well!',
            created_at: `${new Date(Date.now() - 3600000)}`,
            num_comments: -1
        }
        // Over 1-year-old
        const testEntryLastYear: entry = {
            title: 'This is a fake article as well!',
            created_at: `${new Date(Date.now() - (36000000000))}`,
            num_comments: -1
        }
        // Make sure all 3 are correctly detected
        assert.strictEqual(isWithinYear(testEntry_now), true)
        assert.strictEqual(isWithinYear(testEntryHourBefore), true)
        assert.strictEqual(isWithinYear(testEntryLastYear), false)

    }
)

// Test that our titles are being detected correctly
test("Article Type Detection", () => {
    assert.strictEqual(isCorrectArticleType({title: 'Ask HN: Who is hiring?', num_comments: 0, created_at: ""}), true)
    assert.strictEqual(isCorrectArticleType({title: 'Ask HN: Where is hiring?', num_comments: 0, created_at: ""}), false)
    assert.strictEqual(isCorrectArticleType({title: 'This should fail!', num_comments: 0, created_at: ""}), false)

})