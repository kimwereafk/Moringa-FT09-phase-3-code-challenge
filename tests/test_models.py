import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.setup import create_tables

class TestModels(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        create_tables()

    def test_author_creation(self):
        author = Author("John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_magazine_creation(self):
        magazine = Magazine("Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

    def test_article_creation(self):
        author = Author("Jane Smith")
        magazine = Magazine("Health Weekly", "Health")
        article = Article(author, magazine, "Healthy Living Tips")
        self.assertEqual(article.title, "Healthy Living Tips")

if __name__ == "__main__":
    unittest.main()
