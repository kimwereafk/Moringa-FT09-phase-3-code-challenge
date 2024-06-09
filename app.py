from models.author import Author
from models.magazine import Magazine
from models.article import Article
from database.setup import create_tables
from database.connection import get_db_connection

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")

    # Create instances of Author, Magazine, and Article
    author = Author(author_name)
    magazine = Magazine(magazine_name, magazine_category)
    article = Article(author, magazine, article_title)

    # Save instances to the database
    author.save()
    magazine.save()
    article.save()

    # Display results
    print("\nMagazines:")
    for mag in Magazine.all():
        print(f"ID: {mag.id}, Name: {mag.name}, Category: {mag.category}")

    print("\nAuthors:")
    for auth in Author.all():
        print(f"ID: {auth.id}, Name: {auth.name}")

    print("\nArticles:")
    for art in Article.all():
        print(f"ID: {art.id}, Title: {art.title}, Author ID: {art.author.id}, Magazine ID: {art.magazine.id}")

if __name__ == "__main__":
    main()
