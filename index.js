import jsonfile from "jsonfile";
import moment from "moment";
import simpleGit from "simple-git";
import random from "random";

const path = "./data.json";
const startDate = moment("2022-06-04", "YYYY-MM-DD");
const endDate = moment("2024-12-10", "YYYY-MM-DD");

const isWeekday = (date) => {
  const day = date.isoWeekday();
  return day >= 1 && day <= 5; // Monday to Friday
};

const getRandomDateWithinRange = () => {
  const randomDays = random.int(0, endDate.diff(startDate, "days"));
  const date = moment(startDate).add(randomDays, "days");
  return isWeekday(date) ? date : getRandomDateWithinRange();
};

const makeCommits = (n) => {
  if (n <= 0) return simpleGit().push();

  const date = getRandomDateWithinRange().format();
  let commits = random.int(1, 5); // 1–5 commits per day for balance

  const commitData = () => {
    if (commits-- <= 0) return makeCommits(--n);

    const data = { date };
    jsonfile.writeFile(path, data, () => {
      simpleGit().add([path]).commit(date, { "--date": date }, commitData);
    });
  };

  commitData();
};

// Increase total commits to 300–500 for better coverage
makeCommits(1500);
