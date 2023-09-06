import ebooklib
from ebooklib import epub


class EpubReader:
    def __init__(self, epub_filepath) -> None:
        book = epub.read_epub(epub_filepath)

        self.title = book.get_metadata("DC", "title")[0][0]

        self.author = book.get_metadata("DC", "creator")[0][0]

        for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            if "cover" in str(image):
                self.image_content = image.content


d = EpubReader("pel.epub")
