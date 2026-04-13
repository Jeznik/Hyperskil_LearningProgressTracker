import re


class LearningProgressTracker:

    def __init__(self):
        pass

    def run(self):
        print("Learning Progress Tracker")
        while True:
            try:
                usr_cmd = input().strip()
            except EOFError:
                print("Bye!")
                break

            if not usr_cmd:
                print("No input")
                continue

            if usr_cmd == 'exit':
                print("Bye!")
                break

            self.handle_command(usr_cmd)

    def handle_command(self, command):
        if command == 'add students':
            self.add_students()
            return

        if command == 'back':
            print("Enter 'exit' to exit the program")
            return

        print("Unknown command!")

    def add_students(self):
        print("Enter student credentials or 'back' to return")
        students_added = 0
        while True:
            usr_input = input().strip()
            if usr_input == 'back':
                print(f"Total {students_added} students have been added.")
                break

            if self.validate_student_details(usr_input):
                students_added += 1
                print("The student has been added.")

    def validate_student_details(self, user_details):
        regex = r'^([A-Za-z](?:[A-Za-z]|[\'-](?=[A-Za-z]))*[A-Za-z](?:\s+[A-Za-z](?:[A-Za-z]|[\'-](?=[A-Za-z]))*[A-Za-z])*)\s+([^@\s]+@[^@\s]+\.[A-Za-z0-9]+)$'
        if re.match(regex, user_details):
            return True
        else:
            split_details = user_details.split()
            if len(split_details) <= 2:
                print("Incorrect credentials.")
                return False
            email_regex = r'[^@\s]+@[^@\s]+\.[A-Za-z0-9]+$'
            if not re.match(email_regex, split_details[-1]):
                print("Incorrect email.")
                return False
            first_name_regex = r'^[A-Za-z](?:[A-Za-z]|[\'-](?=[A-Za-z]))*[A-Za-z]$'
            if not re.match(first_name_regex, split_details[0]):
                print("Incorrect first name.")
                return False
            else:
                print("Incorrect last name.")
                return False

def main():
    tracker = LearningProgressTracker()
    tracker.run()

if __name__ == '__main__':
    main()
