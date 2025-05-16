# weblinks cli browser
# python weblinks.py  | depends on > pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import textwrap
import os
import sys

ALLOWED_EXTENSIONS={".pdf", ".jpg", ".png", ".txt", ".zip"}

def fetch_page(url):
    try:
        response=requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error: {e}" # bad status code

def parse_page(html):
    soup=BeautifulSoup(html, "html.parser")
    raw_text=soup.get_text("\n", strip=True) # preserve meaningful newlines
    # collect hpyerlinks to dictionary
    links={link.get_text(strip=True): link.get("href") for link in soup.find_all("a") if link.get("href")}
    return raw_text, links

def show_help():
    help_text="""
    Available Commands:
    - visit <link_text>         : Navigate to herplink by its displayed text.
    - save <url>                : Download a file from given URL.
    - save_as  '<path>' <url>   : Save a file to specified folder.
    - exit                      : Quit browser
    
    Example Usage:
    > visit Contact Us
    > save https://example.com/file.pdf
    > save_as 'C:/Downloads' https://example.com/image.png
    """
    print(help_text)

def download_file(url, save_path="downloaded_file"):
    try:
        response=requests.get(url, stream=True)
        response.raise_for_status()
        filename=url.split("/")[-1] or "downloaded_file" 
        
        if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            print(f"Skipping: {filename} (Unsupported file type)")
            return
        
        filepath=os.path.join(save_path, filename)
        
        # Request the file with streaming
        response=requests.get(url, stream=True)
        response.raise_for_status()
        
        # get file size for progress
        total_size=int(response.headers.get("content-length", 0))
        downloaded_size=0
        
        os.makedirs(save_path, exist_ok=True)
        
        with open(filepath, "wb") as file:
            for chunk in repsonse.iter_contents(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    
                    percent=(downloaded_size/total_size) * 100 if total_size> 0 else 0
                    sys.stdout.write(f"\rDownloading {filename} [{percent:.1f}%]")
                    sys.stdout.flush()
        
        print(f"\n File saved to: {filepath}")
        
    except requests.RequestException as e:
        print(f"Download failed: {e}")

def cli_browser():
    current_url=""
    while True:
        command=input("Enter command (or 'exit'): ").strip()
        if command.lower()=="exit":
            break
        elif command.startswith("visit "):
            link_text=command[6:].strip()
            if link_text in links:
                new_url=links[link_text]
                current_url=new_url if new_url.startswith("http") else f"{current_url}/{new_url}"
                html = fetch_page(current_url)
                parsed_text, links=parse_page(html)
                print(parsed_text[:2000]) # display text
            else:
                print("Link not found.")
        elif command.startswith("save "):
            link_text=command[5:].strip()
            if link_text in links:
                file_url = links[link_text]
                file_url = file_url if file_url.startswith("http") else f"{current_url}/{file_url}"
                download_file(file_url)
            else:
                print("File link not found")
        elif command.startswith("save_as '"):
            parts=command.split("'")
            if len(parts) >=3:
                url=parts[2].strip()
                curtom_path=parts[1].strip()
                download_file(url,custom_path)
            else:
                print("Invalid syntax. Use: save_as 'path' url")
        elif command.startswith("help"):
            show_help()
        else:
            current_url=command
            html=fetch_page(current_url)
            parsed_text, links=parse_page(html)
            print(parsed_text[:2000]) 
            print("\nAvailable links:")
            for link in links.keys():
                print(f" - {link}")

cli_browser()