weblinks - text-based web browser for cli
py depends-> pip install requests beautifulsoup4

Available Commands:
    - visit <link_text>         : Navigate to herplink by its displayed text.
    - save <url>                : Download a file from given URL.
    - save_as  '<path>' <url>   : Save a file to specified folder.
    - exit                      : Quit browser
    
    Example Usage:
    > visit Contact Us
    > save https://example.com/file.pdf
    > save_as 'C:/Downloads' https://example.com/image.png
