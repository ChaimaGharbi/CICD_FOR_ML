import base64

with open("Results/model_results.png", "rb") as image_file:
  encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
  
  
report_content = f"""
## Confusion Matrix Ploot
![Confusion Matrix](data:image/png;base64,{encoded_string})
"""

with open("report.md", "a") as report_file:
  report_file.write(report_content)