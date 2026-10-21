import urllib.request
from html.parser import HTMLParser

class PyTorchIndexParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

def check_pytorch_nightly():
    try:
        url = "https://download.pytorch.org/whl/nightly/torch/"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            parser = PyTorchIndexParser()
            parser.feed(html)
            
            cu_versions = set()
            for link in parser.links:
                if 'cu' in link and 'cp312' in link and 'win_amd64' in link:
                    # extract cu version e.g. cu124, cu126, cu128
                    parts = link.split('/')
                    if len(parts) > 1:
                        cu_ver = parts[1]
                        cu_versions.add(cu_ver)
                    elif 'cu' in link:
                        import re
                        m = re.search(r'cu\d+', link)
                        if m:
                            cu_versions.add(m.group(0))
            print("Available nightly CUDA versions for Windows Python 3.12:")
            for v in sorted(cu_versions):
                print(v)
    except Exception as e:
        print(f"Failed to fetch PyTorch index: {e}")

if __name__ == "__main__":
    check_pytorch_nightly()
