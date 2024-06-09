from models.author import Author
from models.article import Article

def delete_articles_by_author(author_name):
    author = Author.get_by_name(author_name)
    if author:
        Article.delete_articles_by_author(author.id)
        print(f"All articles by {author_name} have been deleted.")
    else:
        print(f"Author {author_name} not found.")

if __name__ == "__main__":
    author_name = input("Enter the name of the author whose articles you want to delete: ")
    delete_articles_by_author(author_name)
