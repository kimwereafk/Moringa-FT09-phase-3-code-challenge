from database.connection import get_db_connection

class Author:
    def __init__(self, name, id=None):
        self._name = name
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def save(self):
        if self._id is None:
            self._create_author()
        else:
            self._update_author()

    def _create_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def _update_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE authors SET name = ? WHERE id = ?', (self._name, self._id))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE author_id = ?', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [article[0] for article in articles]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT m.name 
            FROM articles a 
            JOIN magazines m ON a.magazine_id = m.id 
            WHERE a.author_id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return [magazine[0] for magazine in magazines]

    @classmethod
    def all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM authors')
        authors = cursor.fetchall()
        conn.close()
        return [cls(author[1], author[0]) for author in authors]

    @staticmethod
    def get_by_id(author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM authors WHERE id = ?', (author_id,))
        author = cursor.fetchone()
        conn.close()
        return Author(author[1], author[0]) if author else None

    def get_by_name(author_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM authors WHERE name = ?', (author_name,))
        author = cursor.fetchone()
        conn.close()
        return Author(author[1], author[0]) if author else None


    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM authors WHERE id = ?', (self._id,))
        conn.commit()
        conn.close()