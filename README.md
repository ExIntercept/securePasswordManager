If a unique username is entered along with a password, it is saved to details.csv. A salt which is a unique 10 digit randomly generated string, is added to the password, then it is converted to hash using "SHA256" encoding and saved in the csv.
This way even if the csv is compromised, the password cannot be retrieved.
