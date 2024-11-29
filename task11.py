import os

def display_menu():

    print("\n=== Task Menu ===")
    print("1. Task 1: Print 'Hello World'")
    print("2. Task 2: Calculate sum of numbers from 1 to n")
    print("3. Task 3: Show string length, word count, and character count")
    print("4. Task 4: Create a dictionary of words and their lengths")
    print("5. Task 5: Handle number or string input")
    print("6. Task 6: Read a file and show string info")
    print("7. Task 7: Reverse string from a file and save to a new file")
    print("8. Task 8: Generate JSON files for Pokemon from CSV")
    print("9. Task 9: Search Pokemon by ID or Name")
    print("10. Task 10: Export Pokemon with names matching a search term")
    print("0. Exit")
    print("===================")

def run_task(task_number):

    if task_number == "1":
        os.system("python task1.py")
    elif task_number == "2":
        os.system("python task2.py")
    elif task_number == "3":
        os.system("python task3.py")
    elif task_number == "4":
        os.system("python task4.py")
    elif task_number == "5":
        os.system("python task5.py")
    elif task_number == "6":
        os.system("python task6.py")
    elif task_number == "7":
        os.system("python task7.py")
    elif task_number == "8":
        os.system("python task8.py")
    elif task_number == "9":
        os.system("python task9.py")
    elif task_number == "10":
        os.system("python task10.py")
    else:
        print("Invalid choice. Please select a valid task.")

def main():

    while True:
        display_menu()
        choice = input("Enter the task number to run (or 0 to exit): ").strip()
        
        if choice == "0":
            print("Exiting the program. Goodbye!")
            break
        else:
            run_task(choice)

if __name__ == "__main__":
    main()