from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, author, magazine, title, id=None):
        self._author = author
        self._magazine = magazine
        self._title = title
        self._id = id

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self._id is None:
            # Insert new article
            cursor.execute('INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)',
                            (self._title, self._author.id, self._magazine.id))
            self._id = cursor.lastrowid
        else:
            # Update existing article
            cursor.execute('UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?',
                            (self._title, self._author.id, self._magazine.id, self._id))
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    @classmethod
    def all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, author_id, magazine_id FROM articles')
        articles = cursor.fetchall()
        conn.close()
        return [cls(Author.get_by_id(article[2]), Magazine.get_by_id(article[3]), article[1], article[0]) for article in articles]

    @staticmethod
    def get_by_id(article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, author_id, magazine_id FROM articles WHERE id = ?', (article_id,))
        article = cursor.fetchone()
        conn.close()
        return Article(Author.get_by_id(article[2]), Magazine.get_by_id(article[3]), article[1], article[0]) if article else None
    
    @staticmethod
    def delete_articles_by_author(author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM articles WHERE author_id = ?', (author_id,))
        conn.commit()
        conn.close()

    def delete(self):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM articles WHERE id = ?', (self._id,))
            conn.commit()
            conn.close()
