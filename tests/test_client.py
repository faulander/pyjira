import httpx
import pytest
import respx

from pyjira import AsyncJiraClient, JiraClient
from pyjira.resources.issues import AsyncIssueResource, IssueResource


def test_client_requires_domain_or_base_url():
  with pytest.raises(ValueError, match='Either domain or base_url'):
    JiraClient(email='a@b.com', api_token='tok')


def test_client_from_domain():
  with respx.mock:
    client = JiraClient(domain='myco', email='a@b.com', api_token='tok')
    assert client.config.base_url == 'https://myco.atlassian.net'
    client.close()


def test_client_from_base_url():
  with respx.mock:
    client = JiraClient(base_url='https://custom.example.com/', email='a@b.com', api_token='tok')
    assert client.config.base_url == 'https://custom.example.com'
    client.close()


def test_client_has_resource_attributes():
  with respx.mock:
    client = JiraClient(domain='test', email='a@b.com', api_token='tok')
    assert isinstance(client.issues, IssueResource)
    assert hasattr(client, 'projects')
    assert hasattr(client, 'search')
    assert hasattr(client, 'users')
    assert hasattr(client, 'comments')
    client.close()


def test_client_context_manager():
  with respx.mock:
    with JiraClient(domain='test', email='a@b.com', api_token='tok') as client:
      assert isinstance(client, JiraClient)


@pytest.mark.asyncio
async def test_async_client_context_manager():
  async with AsyncJiraClient(domain='test', email='a@b.com', api_token='tok') as client:
    assert isinstance(client.issues, AsyncIssueResource)


@pytest.mark.asyncio
async def test_async_client_requires_domain_or_base_url():
  with pytest.raises(ValueError, match='Either domain or base_url'):
    AsyncJiraClient(email='a@b.com', api_token='tok')
