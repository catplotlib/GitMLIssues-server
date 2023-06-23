from django.core.management.base import BaseCommand
import json
import requests
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
                # Create or update a project model
                Project.objects.update_or_create(
                    repository=project_data['repo'],
                    defaults={
                        # Fetch description from the GitHub API
                        'desc': repo_details['description'],
                        'owner': project_data['owner'],
                        # Fetch language from the GitHub API
                        'lang': repo_details['language'],
                        'repo': repo_details['html_url']
                    }
                )
                # Remove old issues
                Issue.objects.filter(repository=project_data['repo']).delete()
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
                issue_count = 0
                for issue in issues:
                    # Skip pull requests
                    if 'pull_request' in issue:
                        continue
                    Issue.objects.create(
                        repository=project_data['repo'],
                        title=issue['title'],
                        # Join labels with a comma
                        labels=", ".join([label['name']
                                         for label in issue['labels']]),
                        owner=issue['user']['login'],
                        url=issue['html_url']
                    )

                    issue_count += 1
                    if issue_count >= 7:
                        break

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
