import pandas as pd

# -----------------------------
# Step 1: Load Excel file
# -----------------------------
excel_file = r"Library_Books.xlsx"
df = pd.read_excel(excel_file)

# Clean columns to remove extra spaces
df.columns = df.columns.str.strip()

# -----------------------------
# Step 2: User input
# -----------------------------
requested_book_name = input("\nEnter the book name to search: ").strip().lower()

# Strip and lowercase Excel Book Name column
df['Book Name Clean'] = df['Book Name'].astype(str).str.strip().str.lower()
df['Author Name Clean'] = df['Author Name'].astype(str).str.strip().str.lower()

# Step 2a: Find all authors for the given book name
matching_books = df[df['Book Name Clean'] == requested_book_name]

if matching_books.empty:
    print("\nNo book found with that name in the Database.")
    exit()

# List authors for confirmation
authors = matching_books['Author Name'].tolist()
print("\nAvailable authors for this book:")
for i, author in enumerate(authors, 1):
    print(f"{i}. {author}")

author_index = int(input("Select the correct author (enter number): "))
selected_author = authors[author_index - 1].strip()

# Step 2b: Get aisle and rack number
book_match = matching_books[matching_books['Author Name'].str.strip() == selected_author]

if not book_match.empty:
    aisle = book_match.iloc[0]['Aisle Number']
    rack = book_match.iloc[0]['Rack Number']
    print(f"\nBook found!")
    print(f"Book Name: {requested_book_name.title()}")
    print(f"Author: {selected_author}")
    print(f"Aisle Number: {aisle}")
    print(f"Rack Number: {rack}")
else:
    print("\nBook not found in the Database with the selected author.")
