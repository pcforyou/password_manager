import pyperclip
import random
import string
import os # Needed for checking if 'password.txt' exists

print("\n👋 Hey, I AM HERE TO GUIDE YOU :)")

# --- Function Definitions ---

def creating_password(platform, username, l=20):
    """Generates a strong, random password."""
    # MISTAKE FIXED: Only use random characters for security.
    salted_characters = string.ascii_letters + string.digits + string.punctuation
    # The length 'l' is used as the 'k' for random.choices
    generate_pass = ''.join(random.choices(salted_characters, k=l))
    return generate_pass

def save_my_password(platform, username, generated_pass):
    """Appends the new password details to the file."""
    # MISTAKE FIXED: Use "a" (append) mode to save, not "w" (overwrite).
    details = f"\nPlatform: {platform}\nUsername: {username}\nPassword: {generated_pass}\n{'--' * 15}"
    try:
        with open("password.txt", "a") as file:
            file.write(details)
        print("\n✅ Password is saved successfully in 'password.txt'...........")
    except Exception as e:
        print(f"\n❌ Error saving password: {e}")

def search_password(username, platform):
    """Searches for a password based on platform and username."""
    search_platform_term = f"Platform: {platform}"
    search_username_term = f"Username: {username}"
    found_details = []
    
    try:
        with open("password.txt", "r") as file:
            lines = file.readlines()
            
        # Iterate through the lines to find a match
        for i in range(len(lines)):
            line = lines[i].strip()
            if line == search_platform_term:
                # Check the next line for the username
                if i + 1 < len(lines) and lines[i+1].strip() == search_username_term:
                    # Found platform and username, the password should be the next line
                    if i + 2 < len(lines):
                        password_line = lines[i+2].strip()
                        if password_line.startswith("Password:"):
                            found_details.append(password_line)
                            found_details.append(lines[i].strip()) # Platform
                            found_details.append(lines[i+1].strip()) # Username
                            print("\n🔑 Password Found!")
                            # Print all three lines and copy password to clipboard
                            print(f"\t{found_details[1]}")
                            print(f"\t{found_details[2]}")
                            print(f"\t{found_details[0]}")
                            
                            # Extracting just the password for copying
                            password_to_copy = found_details[0].split(":", 1)[1].strip()
                            pyperclip.copy(password_to_copy)
                            print("\n📋 Password copied to clipboard!")
                            return 

        # Only execute if the loop finishes without finding the details
        print(f"\n❌ Sorry, we can't find your password for '{platform}' with username '{username}'.")
    
    # MISTAKE FIXED: Catching the correct file error.
    except FileNotFoundError:
        print("\n❌ Error: The 'password.txt' file was not found. Have you saved any passwords yet?")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

def delete_password(username, platform):
    """Deletes a specific password entry from the file."""
    search_platform_term = f"Platform: {platform}"
    search_username_term = f"Username: {username}"
    entry_found = False
    
    try:
        with open("password.txt", "r") as file:
            all_lines = file.readlines()

        new_lines = []
        skip_lines = 0
        
        # Core Logic for Deletion: Read, Filter, Overwrite
        for i in range(len(all_lines)):
            line = all_lines[i].strip()
            
            if skip_lines > 0:
                # Skip the lines that belong to the entry being deleted (Platform, Username, Password, Separator)
                skip_lines -= 1
                continue
                
            # Check if this line is the start of the target entry
            if line == search_platform_term:
                if i + 1 < len(all_lines) and all_lines[i+1].strip() == search_username_term:
                    # Found the start of the entry, mark the lines to be skipped (4 lines in total)
                    skip_lines = 3 # Password line, Separator line, and potential blank line before next entry
                    entry_found = True
                    continue # Skip the current 'Platform' line
            
            # If not skipping, keep the line
            new_lines.append(all_lines[i])

        if entry_found:
            # Overwrite the file with the lines that were NOT deleted
            with open("password.txt", "w") as file:
                file.writelines(new_lines)
            print("\n✅ Your password entry is successfully deleted from the file.")
        else:
            print(f"\n⚠️ Could not find an entry for '{platform}' with username '{username}'. Nothing was deleted.")
            
    except FileNotFoundError:
        print("\n❌ Error: The 'password.txt' file was not found. No passwords to delete.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred during deletion: {e}")


# --- Main Program Logic ---

print("I am glad to support you here. What can I do for you? Choose by number:")
options = """
1 - Suggest Strong Password and Save
2 - Search any previous Password
3 - Delete any previous Password
"""
print(options)

try:
    choose_mode = int(input("Which number you decide: "))
except ValueError:
    print("\n❌ Invalid input. Please enter a number (1, 2, or 3).")
    exit()

# --- Main Program Execution ---
# ---

if choose_mode == 1:
    # Suggesting strong Password Here:
    mode_1_platform = input("\nEnter the platform (e.g., Google, Amazon): ")
    mode_1_username = input("Enter your desired username: ")
    suggesting_password = creating_password(mode_1_platform, mode_1_username)
    
    print(f"\nOur Generated password is: \n\t\t\t{suggesting_password}")

    # Saving Password Here:
    pyperclip.copy(suggesting_password)
    print("\n📋 Our suggested password is copied to your clipboard. Try to paste it...")
    
    permit_to_save = input("\nCan we save your password in your own file? Choose [Y/N]: ").strip().upper()
    
    if permit_to_save == "Y":
        print("\nSaving your password in 'password.txt'...")
        save_my_password(mode_1_platform, mode_1_username, suggesting_password)
    else:
        print("\nWe respect your decision. The password was not saved.")

elif choose_mode == 2:
    # Searching Password Here:
    mode_2_platform = input("Enter the Platform (e.g., Google, Amazon): ")
    mode_2_username = input("Enter your Username Here: ")
    search_password(mode_2_username, mode_2_platform)

elif choose_mode == 3:
    # Here we Delete password on file
    mode_3_platform = input("Enter the Platform to delete: ")
    mode_3_username = input("Enter the Username to delete: ")
    delete_password(mode_3_username, mode_3_platform)

else:
    print("\n⚠️ Please select a valid number (1, 2, or 3) and rerun the program.")