import tkinter as tk

class MultiPageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page Tkinter App")
        self.geometry("400x300")

        # Container to hold all pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary to store pages
        self.pages = {}

        # Initialize pages
        for Page in (PageOne, PageTwo):
            page_name = Page.__name__
            page = Page(parent=self.container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Show the first page
        self.show_page("PageOne")

    def show_page(self, page_name):
        """Bring the specified page to the front."""
        page = self.pages[page_name]
        page.tkraise()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="This is Page One", font=("Arial", 16))
        label.pack(pady=20)

        button = tk.Button(self, text="Go to Page Two",
                           command=lambda: controller.show_page("PageTwo"))
        button.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="This is Page Two", font=("Arial", 16))
        label.pack(pady=20)

        button = tk.Button(self, text="Go to Page One",
                           command=lambda: controller.show_page("PageOne"))
        button.pack()


if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()
