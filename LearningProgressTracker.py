import re


class LearningProgressTracker:

    def __init__(self):
        self.students = {}
        self.emails = {}
        self.points = {}

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

        if command == 'list':
            self.list_student_ids()
            return

        if command == 'add points':
            self.add_points()
            return

        if command == 'find':
            self.get_student_points()
            return

        print("Unknown command!")

    def add_students(self):
        print("Enter student credentials or 'back' to return")
        while True:
            usr_input = input().strip()
            if usr_input == 'back':
                print(f"Total {len(self.students)} students have been added.")
                break

            if self.validate_student_details(usr_input):
                self.add_student(usr_input)

    def validate_student_details(self, user_details):
        details_re = re.compile(r'^([A-Za-z](?:[A-Za-z]|[\'-](?=[A-Za-z]))*[A-Za-z](?:\s+[A-Za-z](?:[A-Za-z]|[\'-](?=[A-Za-z]))*[A-Za-z])*)\s+([^@\s]+@[^@\s]+\.[A-Za-z0-9]+)$')
        email_re = re.compile(r'[^@\s]+@[^@\s]+\.[A-Za-z0-9]+$')
        first_name_re = re.compile(r'^[A-Za-z](?:[A-Za-z]|[\'-](?=[A-Za-z]))*[A-Za-z]$')

        if details_re.match(user_details):
            return True
        else:
            split_details = user_details.split()
            if len(split_details) <= 2:
                print("Incorrect credentials.")
                return False
            if not email_re.match(split_details[-1]):
                print("Incorrect email.")
                return False
            if not first_name_re.match(split_details[0]):
                print("Incorrect first name.")
                return False
            else:
                print("Incorrect last name.")
                return False

    def add_student(self, user_details):
        split_details = user_details.split()
        first_name = split_details[0]
        last_name = split_details[1]
        email = split_details[-1]
        if self.check_email_exists(email):
            print("This email is already taken.")
            return

        next_id = len(self.students) + 10000
        self.students[next_id] = {
            'Forename': first_name,
            'Surname': last_name,
            'Email': email
        }

        self.emails[email] = next_id
        self.add_student_points([next_id, '0', '0', '0', '0'])

        print("The student has been added.")

        return

    def check_email_exists(self, email: str):
        return email in self.emails

    def check_student_exists(self, student):
        if re.fullmatch(r"\d+", student) and int(student) in self.students:
            return True
        print(f"No student is found for id={student}.")
        return False

    def list_student_ids(self):
        if len(self.students) == 0:
            print("No students found.")
            return
        print("Students:")
        for email in self.emails:
            print(self.emails[email])
        return

    def add_points(self):
        print("Enter an id and points or 'back' to return:")
        while True:
            usr_input = input().strip()
            if usr_input == 'back':
                break
            if self.validate_points(usr_input):
                split_points = usr_input.split()
                student_id = split_points[0]
                if not self.check_student_exists(student_id):
                    continue
                self.add_student_points(split_points)
                print("Points updated.")
            continue

    def validate_points(self, points):
        points_re = re.compile(r'^[A-Za-z0-9]+\s+\d+\s+\d+\s+\d+\s+\d+$')
        if points_re.match(points):
            return True
        print("Incorrect points format.")
        return False

    def add_student_points(self, student_points: list):
        student_id = student_points[0]
        if int(student_id) not in self.points:
            self.points[int(student_id)] = {
                'Python': int(student_points[1]),
                'DSA': int(student_points[2]),
                'Databases': int(student_points[3]),
                'Flask': int(student_points[4])
            }
        else:
            self.points[int(student_id)]['Python'] += int(student_points[1])
            self.points[int(student_id)]['DSA'] += int(student_points[2])
            self.points[int(student_id)]['Databases'] += int(student_points[3])
            self.points[int(student_id)]['Flask'] += int(student_points[4])
        return

    def get_student_points(self):
        print("Enter an id or 'back' to return:")
        while True:
            usr_input = input().strip()
            if usr_input == 'back':
                break
            if not self.check_student_exists(usr_input):
                continue
            student_points = self.points[int(usr_input)]
            print(f"{usr_input} points: "
                  f"Python={student_points['Python']}; "
                  f"DSA={student_points['DSA']}; "
                  f"Databases={student_points['Databases']}; "
                  f"Flask={student_points['Flask']}")
            continue

def main():
    tracker = LearningProgressTracker()
    tracker.run()

if __name__ == '__main__':
    main()
