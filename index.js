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

const simpleGitInstance = simpleGit();

const makeCommits = async (n) => {
  for (let i = 0; i < n; i++) {
    const date = getRandomDateWithinRange().format();
    const commits = random.int(1, 5); // 1–5 commits per day

    for (let j = 0; j < commits; j++) {
      const data = { date };

      await jsonfile.writeFile(path, data);
      await simpleGitInstance.add([path]);
      await simpleGitInstance.commit(date, { "--date": date });
    }
  }

  await simpleGitInstance.push();
  console.log(`${n} days of commits pushed successfully!`);
};

// Adjust the number of days for balance
makeCommits(1500).catch((err) => console.error("Error during commits:", err));
