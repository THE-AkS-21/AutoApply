from resume_parser import parse_resume

# Replace with the path to your sample resume PDF
resume_path = r"C:\Users\91852\Downloads\Jatin Sharma Resume.pdf"


# Test the parsing function
parsed_data = parse_resume(resume_path)

# Print the parsed data
print("Parsed Resume Data:")
print(f"Name: {parsed_data['name']}")
print(f"Email: {parsed_data['email']}")
print(f"Phone: {parsed_data['phone']}")
print(f"Skills: {', '.join(parsed_data['skills'])}")
