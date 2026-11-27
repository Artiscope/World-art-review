// Checks on the links between entries in content/site.json, run before every build:
// - every numbered source used in an article, portfolio or quiz clue exists;
// - every quiz round uses a photo already in images/, a known artist, three published
//   artists as the other choices, and sourced clues.
// A problem stops the build with a plain list of what to fix.
import fs from "node:fs";

export function checkContent() {
  const c = JSON.parse(fs.readFileSync("content/site.json", "utf8"));
  const sources = c.sources || {};
  const artists = new Map((c.artists || []).map((a) => [a.slug, a]));
  const problems = [];
  const text = JSON.stringify(c);
  for (const m of text.matchAll(/data-src=\\"([^"\\]+)\\"/g)) if (!sources[m[1]]) problems.push("a numbered source is used but not listed under sources: " + m[1]);
  for (const a of c.articles || []) for (const s of a.sources || []) if (!sources[s]) problems.push("the article '" + a.slug + "' lists a source that does not exist: " + s);
  for (const r of (c.quiz && c.quiz.rounds) || []) {
    const where = "quiz round '" + r.id + "'";
    if (!artists.has(r.artist)) problems.push(where + " names an artist without a portfolio: " + r.artist);
    if (!r.image || !fs.existsSync(r.image)) problems.push(where + " uses a photo that is not in images/: " + r.image);
    const choices = r.choices || [];
    if (choices.length !== 3) problems.push(where + " needs exactly three other artists to choose from");
    for (const x of choices) if (!(artists.get(x) || {}).published) problems.push(where + " offers an artist who is not published: " + x);
    if (!(r.src || []).length) problems.push(where + " has no sources for its clues");
    for (const s of r.src || []) if (!sources[s]) problems.push(where + " lists a source that does not exist: " + s);
  }
  if (problems.length) throw new Error("content/site.json has problems to fix:\n- " + [...new Set(problems)].join("\n- "));
}
