from django import template
from bs4 import BeautifulSoup
import markdown

register = template.Library()

@register.filter
def preview(value):
    return "".join(value.split('\n')[:3])

@register.filter
def html_edit(value):
    soup = BeautifulSoup(value, "html.parser")
    
    # Add id to image (for open by click)
    for img in soup.find_all('img'):
        # img['class'] = 'popup-image'
        link = img['src']
        a_tag = soup.new_tag('a')
        a_tag['href'] = link
        a_tag['class'] = 'fancylight popup-btn'
        a_tag['data-fancybox-group'] = 'light'

        img_tag = soup.new_tag('img')
        img_tag['class'] = 'lazy img-fluid'
        img_tag['alt'] = ""
        img_tag['data-src'] = link
        
        a_tag.append(img_tag)
        # img.parent.insert_before(a_tag)
        # img.extract()
        img.replace_with(a_tag)
    
    # Replace all youtube-link to iframe video integrated to html code
    for a in soup.find_all(text="youtube-link"):
        link = a.parent['href']

        div_video_tag = soup.new_tag('div')
        div_video_tag['class'] = 'youtube-video' # Add class for add styles in .css
        div_video_tag['style'] = "position: relative; width: 100%; height: 0; padding-bottom: 56.25%;"

        iframe_tag = soup.new_tag('iframe')
        iframe_tag['src'] = link
        iframe_tag['frameborder'] = '0'
        # iframe_tag['allow'] = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
        iframe_tag['allowfullscreen'] = None
        iframe_tag['class'] = 'youtube-video-type1'
        iframe_tag['style'] = "position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
        

        div_video_tag.append(iframe_tag)
        # a.parent.parent.append(div_video_tag)

        # a.parent.extract() # Remove <a> with href (custom markdown style)
        a.replace_with(div_video_tag)
    

    for link in soup.find_all('a', href=True):
        link['target'] = '_blank'
    
    html_content = str(soup)
    
    return html_content

@register.filter
def custom_markdown(value):
    md_text = value
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite', 'tables'])
    return html