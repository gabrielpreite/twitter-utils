/**
 * @jest-environment jsdom
 */

const fs = require("fs")

const printMatches = require('./soccer')
const printStats = require('./soccer')
const percentuale = require('./soccer')
const printTeams = require('./soccer')
const printLineups = require('./soccer')
const printEvents = require('./soccer')
const printTweets = require('./soccer')
const printImages = require('./soccer')

describe("printMatches", () => {
    test('printMatches to be true', () => {
        fs.readFile(require.resolve('../soccer.json'), "utf8", (err, jsonString) => {
            if (err) {
                console.log("File read failed:", err);
                return;
            }
            partite = jsonString;
            expect(printMatches(partite)).toBe(true);
        });
    })
})

describe("printStats", () => {
    test('printStats to be true', () => {
        fs.readFile(require.resolve('../soccer2.json'), "utf8", (err, jsonString) => {
            if (err) {
                console.log("File read failed:", err);
                return;
            }
            let dettagli = jsonString;
            expect(printStats(dettagli)).toBe(true);
        });
    })
})

describe("percentuale", () => {
    test('gives %', () => {
        expect(percentuale(4, 6)).toEqual(["40%", "60%"]);
        expect(percentuale(0, 0)).toEqual(["0%", "0%"]);
    })
})

describe("printTeams", () => {
    test('printTeams to be true', () => {
        fs.readFile(require.resolve('../soccer2.json'), "utf8", (err, jsonString) => {
            if (err) {
                console.log("File read failed:", err);
                return;
            }
            dettagli = jsonString;
            expect(printTeams(dettagli)).toBe(true);
        });
    })
})

describe("printLineups", () => {
    test('printLineups to be true', () => {
        fs.readFile(require.resolve('../soccer2.json'), "utf8", (err, jsonString) => {
            if (err) {
                console.log("File read failed:", err);
                return;
            }
            dettagli = jsonString;
            expect(printLineups(dettagli)).toBe(true);
        });
    })
})

describe("printEvents", () => {
    test('printEvents to be true', () => {
        fs.readFile(require.resolve('../soccer2.json'), "utf8", (err, jsonString) => {
            if (err) {
                console.log("File read failed:", err);
                return;
            }
            dettagli = jsonString;
            expect(printEvents(dettagli)).toBe(true);
        });
    })
})

describe("printTweets", () => {
    test('printTweets to be true', () => {
        fs.readFile(require.resolve('../soccer3.json'), "utf8", (err, jsonString) => {
            if (err) {
                console.log("File read failed:", err);
                return;
            }
            let results = jsonString;
            expect(printTweets(results)).toBe(true);
        });
    })
})

describe("printImages", () => {
    test('printImages to be true', () => {
        fs.readFile(require.resolve('../soccer3.json'), "utf8", (err, jsonString) => {
            if (err) {
                console.log("File read failed:", err);
                return;
            }
            results = jsonString;
            expect(printImages(results)).toBe(true);
        });
    })
})