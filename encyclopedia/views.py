from django.shortcuts import render, redirect
from .util import get_entry, save_entry, list_entries
import markdown2
import random

# welcome, have one side bar and will list all pages
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })

def entry(request, title):
    entry_content = get_entry(title)

    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "error_message": "The requested page was not found."
        })

    html_content = markdown2.markdown(entry_content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get("q", "")
    entries = list_entries()

    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    if len(matching_entries) == 0:
        return render(request, "encyclopedia/error.html", {
            "error_message": "The requested page was not found."
        })
    elif len(matching_entries) == 1:
        return redirect('entry', title=matching_entries[0])
    else:
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "entries": matching_entries
        })

def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        existing_entry = get_entry(title)
        if existing_entry is not None:
            return render(request, "encyclopedia/error.html", {
                "error_message": "An entry with this title already exists."
            })

        save_entry(title, content)
        return redirect('entry', title=title)

    return render(request, "encyclopedia/newpage.html")

def random_page(request):
    entries = list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)