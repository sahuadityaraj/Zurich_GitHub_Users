import requests
import csv
import os

# GitHub personal access token from environment variables (recommended for security)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Set up headers for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# GitHub API base URL
BASE_URL = "https://api.github.com"

# Function to clean up company names
def clean_company_name(company_name):
    if not company_name:
        return ""
    # Strip leading @ symbol and whitespace
    company_name = company_name.lstrip('@').strip()
    return company_name.upper()

# Function to get users in Zurich with more than 50 followers
def get_users_in_city(city="Zurich", min_followers=50):
    url = f"{BASE_URL}/search/users"
    params = {
        "q": f"location:{city} followers:>{min_followers}",
        "per_page": 100,
        "page": 1
    }
    users = []
    
    while True:
        response = requests.get(url, headers=headers, params=params).json()
        users.extend(response.get("items", []))
        if "next" not in response.get("links", {}):
            break
        params["page"] += 1

    return users

# Function to save user data to users.csv
def save_users_to_csv(users):
    with open("users.csv", "w", newline="") as csvfile:
        fieldnames = ["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for user in users:
            user_details = requests.get(user["url"], headers=headers).json()
            writer.writerow({
                "login": user["login"],
                "name": user_details.get("name", ""),
                "company": clean_company_name(user_details.get("company", "")),
                "location": user_details.get("location", ""),
                "email": user_details.get("email", ""),
                "hireable": user_details.get("hireable", ""),
                "bio": user_details.get("bio", ""),
                "public_repos": user_details.get("public_repos", 0),
                "followers": user_details.get("followers", 0),
                "following": user_details.get("following", 0),
                "created_at": user_details.get("created_at", "")
            })

# Function to save repository data to repositories.csv
def save_repositories_to_csv(users):
    with open("repositories.csv", "w", newline="") as csvfile:
        fieldnames = ["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects", "has_wiki", "license_name"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for user in users:
            repos_url = f"{BASE_URL}/users/{user['login']}/repos"
            params = {"sort": "pushed", "per_page": 100}
            page = 1
            repos = []

            while page <= 5:  # Limit to 500 repositories (5 pages x 100 per page)
                params["page"] = page
                response = requests.get(repos_url, headers=headers, params=params).json()
                repos.extend(response)
                if len(response) < 100:
                    break
                page += 1

            for repo in repos:
                writer.writerow({
                    "login": user["login"],
                    "full_name": repo.get("full_name", ""),
                    "created_at": repo.get("created_at", ""),
                    "stargazers_count": repo.get("stargazers_count", 0),
                    "watchers_count": repo.get("watchers_count", 0),
                    "language": repo.get("language", ""),
                    "has_projects": repo.get("has_projects", False),
                    "has_wiki": repo.get("has_wiki", False),
                    "license_name": repo.get("license", {}).get("key", "")
                })

# Main function to run the data collection
def main():
    print("Fetching users in Zurich with over 50 followers...")
    users = get_users_in_city()
    print(f"Found {len(users)} users. Saving to users.csv...")
    save_users_to_csv(users)
    print("Users saved. Fetching repositories...")
    save_repositories_to_csv(users)
    print("Repositories saved to repositories.csv.")

if __name__ == "__main__":
    main()
