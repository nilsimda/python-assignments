#!/usr/bin/env python3
"""
File: chatbot.py
-------------------
To-Do-Liste
"""

def create_list():
    name = input("What should your list be called? ")
    with open('to_do.txt', 'a') as to_do:
        to_do.write("To-Do List:\n")

        print("Let us add your tasks now!")
        print("If you have added all your tasks type 'quit'.")

        curr_task = ""
        n_task = 1
        while True:
            curr_task = input(f"Task {n_task}: ")
            if curr_task.lower() == 'quit':
                to_do.write(f"Name: {name} Task_number: {n_task}\n")
                return
            to_do.write(f"Task {n_task}: {curr_task}\n")
            n_task += 1
        

def find_list(name):     
    with open("to_do.txt", "r") as to_do:
        for index, line in enumerate(to_do):
            if line.startswith(f"Name: {name} Task_number: "):
                return (index, line)
    return (0, "")

def print_list():
    while (tp:=find_list(input("What's the name of the list you want to print? "))) == (0,""):
        print("Sorry this To-do list does not seem to exist.")

    index, line = tp[0], tp[1]
    start = index - (int(line.split()[3]))
    
    with open("to_do.txt", "r") as to_do:
        lst = to_do.readlines()[start:index]

    for index, t in enumerate(lst):
        if index ==0:
            print("\n")
            print(t, end='')
            print("-"*len(t))
        else:
            print(t, end='')
    print("\n")

def main():
    while True:
        mode = input("Do you want to create or print a To-Do List? ")
        if "quit" in mode.lower():
            print("Finishing...")
            return
        elif "create" in mode.lower():
            create_list()
        elif "print" in mode.lower():
            print_list()
        else:
            print("I dont have that function yet")

if __name__ == '__main__':
    main()
