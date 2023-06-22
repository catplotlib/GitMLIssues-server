from django.core.management.base import BaseCommand
import json
import requests  # Import the requests library
from api.models import Project, Issue
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Command(BaseCommand):
    help = 'Load projects and issues from GitHub API'

    def handle(self, *args, **options):
        with open(BASE_DIR / 'data' / 'data.json', 'r') as file:
            data = json.load(file)
            for project_data in data:
                # Fetch repository details from the GitHub API
                response = requests.get(
                    f"https://api.github.com/repos/{project_data['owner']}/{project_data['repo']}",
                    headers={"Accept": "application/vnd.github.v3+json"}
                )
                # Check that the request was successful
                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(
                        f"Failed to fetch details for {project_data['owner']}/{project_data['repo']}"))
                    continue
                # Parse the response JSON
                repo_details = response.json()
                # Create a project model
                Project.objects.create(
                    repository=project_data['repo'],
                    desc=repo_details['description'],  # Fetch description from the GitHub API
                    owner=project_data['owner'],
                    lang=repo_details['language']  # Fetch language from the GitHub API
                )
                # Fetch issues from the GitHub API
                response = requests.get(
                    f"https://api.github.com/repos/{project_data['owner']}/{project_data['repo']}/issues",
                    headers={"Accept": "application/vnd.github.v3+json"}
                )
                # Check that the request was successful
                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(
                        f"Failed to fetch issues for {project_data['owner']}/{project_data['repo']}"))
                    continue
                # Parse the response JSON
                issues = response.json()
                # Create an issue model for each issue
                for issue in issues[:5]:
                    Issue.objects.create(
                        repository=project_data['repo'],
                        title=issue['title'],
                        # Join labels with a comma
                        labels=", ".join([label['name']
                                          for label in issue['labels']]),
                        owner=issue['user']['login'],
                        url=issue['html_url']
                    )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
