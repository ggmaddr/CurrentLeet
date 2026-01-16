from bs4 import BeautifulSoup
import re

def html_to_markdown(html_element):
    """
    Convert HTML element to markdown format, grouping content by pages.
    
    Each page's first paragraph is converted to a heading 3 (###).
    Page headers are ignored and not included in the output.
    
    Args:
        html_element: HTML string or BeautifulSoup element
        
    Returns:
        str: Markdown formatted text with first paragraph as heading 3 for each page
    """
    # Parse HTML if string is provided
    if isinstance(html_element, str):
        soup = BeautifulSoup(html_element, 'html.parser')
    else:
        soup = html_element
    
    # Find all page headings (h2) first, then get their parent divs
    # This avoids processing nested divs multiple times
    page_headings = soup.find_all('h2', string=re.compile(r'Page \d+ of \d+'))
    
    markdown_output = []
    processed_pages = set()  # Track which pages we've already processed
    
    for page_h2 in page_headings:
        page_match = re.search(r'Page (\d+) of (\d+)', page_h2.get_text())
        if page_match:
            page_num = int(page_match.group(1))
            total_pages = int(page_match.group(2))
            
            # Skip if we've already processed this page
            if page_num in processed_pages:
                continue
            
            # Find the parent div with the DARUcf class
            parent_div = page_h2.find_parent('div', class_=re.compile(r'DARUcf'))
            
            if parent_div:
                processed_pages.add(page_num)
                
                # Collect all paragraph text from this div only
                para_texts = []
                for p in parent_div.find_all('p', class_=re.compile(r'ndfHFb-c4YZDc-cYSp0e-DARUcf-Df1ZY-eEGnhe')):
                    text = p.get_text(strip=True)
                    if text and text != 'Recap':  # Skip the Recap heading itself
                        para_texts.append(text)
                
                # Add body content
                if para_texts:
                    # Make the first paragraph a heading 3
                    first_para = para_texts[0]
                    markdown_output.append(f"\n#### {first_para}  \n")
                    
                    # Add the rest as regular paragraphs with two trailing spaces for line breaks
                    if len(para_texts) > 1:
                        # Add two spaces at the end of each line
                        formatted_paras = [para + "  " for para in para_texts[1:]]
                        markdown_output.append("\n".join(formatted_paras))
                
                # Add blank line between pages
                markdown_output.append("")
    
    return "\n".join(markdown_output).strip()

# Example usage:
# Read HTML string from external file
with open('webTextExtract-input.txt', 'r', encoding='utf-8') as f:
    html_string = f.read()

markdown = html_to_markdown(html_string)

# Write output to file
with open('webTextExtract-output.md', 'w', encoding='utf-8') as f:
    f.write(markdown)

