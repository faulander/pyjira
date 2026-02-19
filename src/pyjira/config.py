from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class JiraConfig:
  """Configuration for the Jira API client."""

  base_url: str
  email: str
  api_token: str
  timeout: float = 30.0
  max_retries: int = 3
  default_headers: dict[str, str] = field(default_factory=dict)

  @classmethod
  def from_domain(
    cls,
    domain: str,
    email: str,
    api_token: str,
    **kwargs: object,
  ) -> JiraConfig:
    """Create config from an Atlassian domain name.

    Args:
      domain: The Atlassian domain (e.g. 'mycompany' for mycompany.atlassian.net)
      email: Account email address
      api_token: Jira API token
      **kwargs: Additional config options
    """
    base_url = f'https://{domain}.atlassian.net'
    return cls(base_url=base_url, email=email, api_token=api_token, **kwargs)  # type: ignore[arg-type]
