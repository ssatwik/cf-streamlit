# Codeforces Lockout

## Overview

Codeforces Lockout is a competitive programming format where participants go head-to-head to solve a set of problems. Once a participant solves a problem, it becomes "locked out" for their opponent, meaning they can no longer earn points for solving it. The player with the highest points at the end of the match wins.

## How It Works

1. Codeforces problems are retrieved based on user-specified ratings.

2. Problems already solved by any participant are filtered out to ensure fairness.

3. Problem data is collected through web scraping from Codeforces, while solved problems for each user are fetched via the Codeforces API.

4. When a participant solves a problem, the corresponding cell turns green for them and red for opponents, indicating that it is now locked.

5. Opponents cannot earn points for solving locked-out problems.

6. The match continues until all problems are solved or the timer runs out. The participant with the highest score at the end wins.
