
class Book:
    def init(self, title:str, author:str):
        self.title = title
        self.author = author
    def display(self):
        print(self.title, self.author)

livre = Book("le petit prince", "antoine de saint-exupery")





livre.display()


