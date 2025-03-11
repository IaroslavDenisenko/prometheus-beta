import os
import requests

def download_file(url, destination=None):
    """
    Download a file from a given URL.

    Args:
        url (str): The URL of the file to download.
        destination (str, optional): The local path to save the file. 
                                     If not provided, uses the filename from the URL.

    Returns:
        str: The local path where the file was saved.

    Raises:
        ValueError: If the URL is invalid or empty.
        IOError: If there's an error downloading or saving the file.
    """
    # Validate URL
    if not url or not isinstance(url, str):
        raise ValueError("Invalid URL: URL must be a non-empty string")

    try:
        # Send a GET request to download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Determine destination path
        if destination is None:
            # Extract filename from URL or Content-Disposition header
            filename = response.headers.get('Content-Disposition')
            if filename:
                filename = filename.split('filename=')[-1].strip('"\'')
            else:
                filename = url.split('/')[-1]
            
            # Use current working directory if no path specified
            destination = os.path.join('downloads', filename)

        # Create downloads directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        # Write the file
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return destination

    except requests.RequestException as e:
        raise IOError(f"Error downloading file from {url}: {str(e)}")
    except Exception as e:
        raise IOError(f"Unexpected error saving file: {str(e)}")