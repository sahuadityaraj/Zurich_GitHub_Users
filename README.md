- **Data Collection Method**: This project uses the GitHub API to retrieve data on users in Zurich with over 50 followers, along with details on their repositories.
- **Interesting Finding**: Many Zurich-based developers are proficient in multiple languages, with a surprising number contributing to open-source projects in Python.
- **Recommendation for Developers**: Growing a follower base is highly correlated with regular contributions to repositories in trending languages, so engage consistently!

### Project Overview

This project retrieves GitHub user information for Zurich-based developers with over 50 followers, including their public repositories. The data is saved in two CSV files:

- `users.csv`: Contains user profile details.
- `repositories.csv`: Contains repository information for each user.

### Files
- **users.csv**: Holds data such as username, company, location, number of followers, and repository count.
- **repositories.csv**: Lists the repositories associated with each user, along with details like stars, language, and creation date.

### Data Collection Script
- `data_collection.py`: A Python script that fetches user and repository data, cleans company names, and saves the output to `users.csv` and `repositories.csv`.

### Running the Script
1. Set up your GitHub token as an environment variable for security.
2. Run `data_collection.py` to automatically generate `users.csv` and `repositories.csv`.

### Usage
Use this dataset to analyze Zurich's developer ecosystem, popular languages, or trends in repository contributions.
