from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self._name = name
        self._category = category
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def save(self):
        if self._id is None:
            self._create_magazine()
        else:
            self._update_magazine()

    def _create_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def _update_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET name = ?, category = ? WHERE id = ?', (self._name, self._category, self._id))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [article[0] for article in articles]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT au.name 
            FROM articles a 
            JOIN authors au ON a.author_id = au.id 
            WHERE a.magazine_id = ?
        ''', (self._id,))
        contributors = cursor.fetchall()
        conn.close()
        return [contributor[0] for contributor in contributors]

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self._id,))
        titles = cursor.fetchall()
        conn.close()
        return [title[0] for title in titles] if titles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT au.name 
            FROM articles a 
            JOIN authors au ON a.author_id = au.id 
            WHERE a.magazine_id = ?
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [author[0] for author in authors] if authors else None

    @classmethod
    def all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, category FROM magazines')
        magazines = cursor.fetchall()
        conn.close()
        return [cls(magazine[1], magazine[2], magazine[0]) for magazine in magazines]  

    @staticmethod
    def get_by_id(magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, category FROM magazines WHERE id = ?', (magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        return Magazine(magazine[1], magazine[2], magazine[0]) if magazine else None

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM magazines WHERE id = ?', (self._id,))
        conn.commit()
        conn.close()