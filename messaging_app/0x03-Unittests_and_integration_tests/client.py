#!/usr/bin/env python3
"""
Client module
"""
from utils import get_json


class GithubOrgClient:
    """
    GithubOrgClient class
    """
    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        """
        Initialize GithubOrgClient
        """
        self._org_name = org_name

    @property
    def org(self):
        """
        Get org data
        """
        return get_json(self.ORG_URL.format(self._org_name))

    @property
    def _public_repos_url(self):
        """
        Get public repos url
        """
        return self.org["repos_url"]

    @property
    def public_repos(self):
        """
        Get public repos
        """
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]

    def has_license(self, repo, license_key):
        """
        Check if repo has license
        """
        return repo.get("license", {}).get("key") == license_key
