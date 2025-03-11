import os
import pytest
import requests
import tempfile
import shutil

from src.file_downloader import download_file

class MockResponse:
    def __init__(self, url, status_code=200, content=b'test content', headers=None):
        self.url = url
        self.status_code = status_code
        self._content = content
        self.headers = headers or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP Error {self.status_code}")

    def iter_content(self, chunk_size):
        yield self._content

def test_download_file_default_destination(monkeypatch):
    # Temporary directory for test downloads
    test_dir = tempfile.mkdtemp()
    
    # Mock requests.get
    def mock_get(url, stream=True):
        return MockResponse(url, content=b'test download content')
    monkeypatch.setattr(requests, 'get', mock_get)

    try:
        # Use a temp directory for downloads
        monkeypatch.chdir(test_dir)
        os.makedirs('downloads', exist_ok=True)

        # Test download
        url = 'http://example.com/testfile.txt'
        filepath = download_file(url)

        # Verify file was downloaded
        assert os.path.exists(filepath)
        assert os.path.basename(filepath) == 'testfile.txt'
        
        # Verify file content
        with open(filepath, 'rb') as f:
            assert f.read() == b'test download content'

    finally:
        # Clean up temporary directory
        shutil.rmtree(test_dir)

def test_download_file_custom_destination(monkeypatch):
    # Temporary directory for test downloads
    test_dir = tempfile.mkdtemp()
    
    try:
        # Mock requests.get
        def mock_get(url, stream=True):
            return MockResponse(url, content=b'custom content')
        monkeypatch.setattr(requests, 'get', mock_get)

        # Use a temp directory
        monkeypatch.chdir(test_dir)

        # Test download with custom destination
        url = 'http://example.com/customfile.txt'
        custom_path = os.path.join(test_dir, 'custom_downloads', 'myfile.txt')
        filepath = download_file(url, custom_path)

        # Verify file was downloaded to correct location
        assert filepath == custom_path
        assert os.path.exists(filepath)
        
        # Verify file content
        with open(filepath, 'rb') as f:
            assert f.read() == b'custom content'

    finally:
        # Clean up temporary directory
        shutil.rmtree(test_dir)

def test_download_file_invalid_url():
    # Test invalid URL inputs
    with pytest.raises(ValueError, match="Invalid URL"):
        download_file(None)
    with pytest.raises(ValueError, match="Invalid URL"):
        download_file("")
    with pytest.raises(ValueError, match="Invalid URL"):
        download_file(123)  # Non-string input

def test_download_file_network_error(monkeypatch):
    # Simulate network error
    def mock_get(url, stream=True):
        raise requests.ConnectionError("Network error")
    monkeypatch.setattr(requests, 'get', mock_get)

    with pytest.raises(IOError, match="Error downloading file"):
        download_file('http://example.com/nonexistent.txt')

def test_download_file_http_error(monkeypatch):
    # Simulate HTTP error
    def mock_get(url, stream=True):
        response = MockResponse(url, status_code=404)
        response.raise_for_status()
        return response
    monkeypatch.setattr(requests, 'get', mock_get)

    with pytest.raises(IOError, match="Error downloading file"):
        download_file('http://example.com/404.txt')