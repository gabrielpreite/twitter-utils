/**
 * @jest-environment jsdom
 */

const showLeaderBoard = require('./fantacitorio')

const fs = require("fs");

describe("showLeaderboard", () => {
    test('showLeaderboard to be true', () => {
        fs.readFile(require.resolve('../PunteggiFantacitorio.json'), "utf8", (err, jsonString) => {
            if (err) {
                console.log("File read failed:", err);
                return;
            }
            let partite = jsonString;
            expect(showLeaderBoard(partite)).toBe(true);
        });
    })
})