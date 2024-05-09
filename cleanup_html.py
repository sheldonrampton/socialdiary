# Doesn't preserve paragraph or line breaks.

from bs4 import BeautifulSoup

def strip_html(html_content):
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Extract text from the parsed HTML
    text = soup.get_text(separator=' ', strip=True)
    return text

# Example usage:
html_message = """
<html><head></head><body class="ApplePlainTextBody" style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space; ">Sure, time permitting.<div><br><div class="AppleOriginalContents"><div>On Dec 21, 2009, at 10:15 PM, David Klann wrote:</div><br class="Apple-interchange-newline"><blockquote type="cite"><span class="Apple-style-span" style="border-collapse: separate; font-family: Helvetica; font-size: medium; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-border-horizontal-spacing: 0px; -webkit-border-vertical-spacing: 0px; -webkit-text-decorations-in-effect: none; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; ">I agree. I'll pass your comments on to our site developer. Would you<br>be open to the idea of meeting again with him and with me?<br></span></blockquote></div><br></div><br><br><div id="AppleMailSignature">--------------------------------<br>Sheldon Rampton<br>713 W. Carroll Street<br>Portage, WI 53901<br>(608) 742-8408<br>mobile: (608) 206-2745<br>email: sheldon@sheldonrampton.com<br><br><br><br><br></div><br></body></html>
"""
plain_text = strip_html(html_message)
print(plain_text)
