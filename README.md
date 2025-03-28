Codeforces Lockout Bot
Overview

Codeforces Lockout is a competitive programming format where participants go head-to-head to solve a set of problems. Once a participant solves a problem, it becomes "locked out" for their opponent, meaning they can no longer earn points for solving it. The player with the highest points at the end of the match wins.
How It Works

    Problem Selection:

        The bot retrieves problems of user-specified ratings from Codeforces.

        Problems already solved by any participant are filtered out to ensure fairness.

    Fetching Data:

        Problem data is obtained through web scraping from Codeforces.

        Solved problems for each user are fetched using the official Codeforces API.

    Lockout Mechanism:

        When a participant solves a problem, the corresponding cell turns green for them and red for opponents, indicating that it is now locked out.

        Opponents cannot earn points for solving locked-out problems.

    Winner Determination:

        The match continues until all problems are solved or the timer runs out.

        The participant with the highest points at the end is declared the winner.
