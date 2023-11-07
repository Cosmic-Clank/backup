from django.shortcuts import render
from django.http import HttpResponse
import os
# View function
def index(request):
    # Path to the file - adjust the path as needed
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_path = os.path.join(BASE_DIR, 'logs', "ganache-20231103-134515.log")
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()  # Reading the content of the file
            
            # Optionally, you could limit the amount of content displayed
            # For example, to display only the first 1000 characters:
            # content = content[:1000]

    except FileNotFoundError:
        content = "File not found."
        # Handle the error as you see fit

    # Pass the file name and content to the template
    context = {
        'file_name': os.path.basename(file_path),
        'content': content,
    }
    
    if request.method == 'POST':
        
        from fuzzylogic.fuzzycode import fuzzylogic
        result, data = fuzzylogic.main(file_path)
        # result = "96.66%"
        message = "Indicating that there os a high risk of fradulant activity in the log files"
        # Return a response or redirect after analysis
        print(result, type(result))
        return render(request, "fuzzylogic/analysis.html", {"result": f"{result:.2f}%", "message": message, "fradulant_data": data})
    
    # Render the template with the context
    return render(request, 'fuzzylogic/index.html', context)