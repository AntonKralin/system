from bs4 import BeautifulSoup
import requests
#import ebooklib
import time
from ebooklib import epub


book_name = "verhovnyj-mag"
http_url = "https://jaomix.ru/verhovnyj-mag/glava-0-1-prolog/"
next_but = {'name': 'li', 'class': 'next'}
attr = 'href'
#save_el = {'name': 'div', 'class': 'entry themeform'}
save_el = {'name': 'div', 'class': 'post-wrapper group', 'text': 'entry themeform'}


def get_text(response: requests.Response, save_el: dict):
    bs = BeautifulSoup(response.text, "html.parser")
    r_set = bs.findAll(save_el.get('name'), save_el.get('class'))
    r_result = ""
    for r_elem in r_set:
        text = r_elem.find_all(save_el.get('name'), save_el.get('text'))
        h_text = r_elem.find_all('h1')
        for i_h in h_text:
            r_result += str(i_h)
        for i_text in text:
            p_text = i_text.find_all("p")
            for i_p in p_text:
                r_result += str(i_p)
    return r_result


def get_next_page(response: requests.Response, next_but: dict, attr: str):
    bs = BeautifulSoup(response.text, "html.parser")
    r_set = bs.findAll(next_but.get('name'), next_but.get('class'))
    next_page = None
    for r_elem in r_set:
        href = r_elem.find_all('a')
        for i_href in href:
            next_page = i_href.get(attr)
    return next_page


def generate_next_chapter(http_url: str, save_el: dict, next_but: dict, attr: str):
    try:
        response = requests.get(http_url)
        chapter = get_text(response, save_el)
        next_page = get_next_page(response, next_but, attr)
        yield chapter
        while next_page:
            response = requests.get(next_page)
            next_page = get_next_page(response, next_but, attr)
            chapter = get_text(response, save_el)
            yield chapter
        else:
            return

    except Exception as exc:
        print(exc)
        return


if __name__ == "__main__":
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title(book_name)
    book.set_language("ru")
    book.add_author("Python")

    style = 'body { font-family: Times, Times New Roman, serif; }'

    nav_css = epub.EpubItem(uid="style_nav",
                            file_name="style/nav.css",
                            media_type="text/css",
                            content=style)
    book.add_item(nav_css)

    gen_ch = generate_next_chapter(http_url, save_el, next_but, attr)
    chapters = []
    i = 0
    for text_ch in gen_ch:
        i += 1
        #print(i)
        #if i % 10 == 0:
        #    time.sleep(5)
        c1 = epub.EpubHtml(title="ch " + str(i),
                           file_name=str(i)+'.xhtml',
                           lang='ru')
        c1.set_content(text_ch)
        book.add_item(c1)
        chapters.append(c1)

    book.toc = (
        epub.Link("intro.xhtml", "intro1", "intro2"),
        (epub.Section("Chapters"), chapters),
    )
    book.spine = ["nav"] + chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(book_name+'.epub', book, {"epub3_pages": False})

