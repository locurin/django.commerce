#custome context processors

def categories_processor(request):
    list_of_categories = ["Electronics", "Fashion",  "Gaming", "Garden",  "Groceries",  "House",   
     "Music", "Pets", "Sports", "Toys", "Vehicles",]
    return {"categs":list_of_categories}