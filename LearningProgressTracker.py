import re
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch


class LearningProgressTracker:
    COURSES = ('Python', 'DSA', 'Databases', 'Flask')
    EMAIL_RE = re.compile(r'[^@\s]+@[^@\s]+\.[A-Za-z0-9]+$')
    NAME_RE = re.compile(r'^[A-Za-z](?:[A-Za-z]|[\'-](?=[A-Za-z]))*[A-Za-z]$')
    POINTS_RE = re.compile(r'^[A-Za-z0-9]+\s+\d+\s+\d+\s+\d+\s+\d+$')

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

            student_details, error = self.parse_student_details(usr_input)
            if error:
                print(error)
                continue
            self.add_student(*student_details)

    def parse_student_details(self, user_details):
        split_details = user_details.split()
        if len(split_details) <= 2:
            return None, "Incorrect credentials."
        if not self.EMAIL_RE.match(split_details[-1]):
            return None, "Incorrect email."
        if not self.NAME_RE.match(split_details[0]):
            return None, "Incorrect first name."
        if not all(self.NAME_RE.match(last_name_part) for last_name_part in split_details[1:-1]):
            return None, "Incorrect last name."
        first_name = split_details[0]
        last_name = ' '.join(split_details[1:-1])
        email = split_details[-1]
        return (first_name, last_name, email), None

    def validate_student_details(self, user_details):
        _, error = self.parse_student_details(user_details)
        if error:
            return False
        return True

    def add_student(self, first_name, last_name, email):
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
        self.add_student_points([next_id, *(['0'] * len(self.COURSES))])

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
            if not self.validate_points(usr_input):
                print("Incorrect points format.")
                continue
            split_points = usr_input.split()
            student_id = split_points[0]
            if not self.check_student_exists(student_id):
                continue
            self.add_student_points(split_points)
            print("Points updated.")
            continue

    def validate_points(self, points):
        if self.POINTS_RE.match(points):
            return True
        return False

    def add_student_points(self, student_points: list):
        student_id = int(student_points[0])
        if student_id not in self.points:
            self.points[student_id] = {course: 0 for course in self.COURSES}

        for course, value in zip(self.COURSES, student_points[1:]):
            self.points[student_id][course] += int(value)
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
            course_points = '; '.join(
                f"{course}={student_points[course]}" for course in self.COURSES
            )
            print(f"{usr_input} points: {course_points}")
            continue

def main():
    tracker = LearningProgressTracker()
    tracker.run()


class LearningProgressTrackerTestCase(unittest.TestCase):

    def setUp(self):
        self.tracker = LearningProgressTracker()

    def capture_output(self, callable_, *args, **kwargs):
        output = StringIO()
        with redirect_stdout(output):
            result = callable_(*args, **kwargs)
        return result, output.getvalue().strip().splitlines()

    def test_validate_student_details_accepts_valid_credentials(self):
        result, output = self.capture_output(
            self.tracker.validate_student_details,
            "John Doe john.doe@example.com"
        )

        self.assertTrue(result)
        self.assertEqual([], output)

    def test_validate_student_details_accepts_multi_part_last_name(self):
        result, output = self.capture_output(
            self.tracker.validate_student_details,
            "Robert Jemison Van de Graaff robertvdgraaff@mit.edu"
        )

        self.assertTrue(result)
        self.assertEqual([], output)

    def test_validate_student_details_rejects_missing_name_part(self):
        result, output = self.capture_output(
            self.tracker.validate_student_details,
            "John john.doe@example.com"
        )

        self.assertFalse(result)
        self.assertEqual([], output)

    def test_validate_student_details_rejects_bad_email(self):
        result, output = self.capture_output(
            self.tracker.validate_student_details,
            "John Doe john.doe@example"
        )

        self.assertFalse(result)
        self.assertEqual([], output)

    def test_validate_student_details_rejects_bad_first_name(self):
        result, output = self.capture_output(
            self.tracker.validate_student_details,
            "-John Doe john.doe@example.com"
        )

        self.assertFalse(result)
        self.assertEqual([], output)

    def test_validate_student_details_rejects_bad_last_name(self):
        result, output = self.capture_output(
            self.tracker.validate_student_details,
            "John -Doe john.doe@example.com"
        )

        self.assertFalse(result)
        self.assertEqual([], output)

    def test_parse_student_details_returns_parsed_names_and_email(self):
        result, error = self.tracker.parse_student_details(
            "Robert Jemison Van de Graaff robertvdgraaff@mit.edu"
        )

        self.assertEqual(("Robert", "Jemison Van de Graaff", "robertvdgraaff@mit.edu"), result)
        self.assertIsNone(error)

    def test_parse_student_details_returns_error_message(self):
        result, error = self.tracker.parse_student_details(
            "John -Doe john.doe@example.com"
        )

        self.assertIsNone(result)
        self.assertEqual("Incorrect last name.", error)

    def test_add_student_stores_student_email_and_initial_points(self):
        _, output = self.capture_output(
            self.tracker.add_student,
            "John",
            "Doe",
            "john.doe@example.com"
        )

        self.assertEqual(["The student has been added."], output)
        self.assertEqual(
            {
                'Forename': 'John',
                'Surname': 'Doe',
                'Email': 'john.doe@example.com'
            },
            self.tracker.students[10000]
        )
        self.assertEqual(10000, self.tracker.emails["john.doe@example.com"])
        self.assertEqual(
            {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0},
            self.tracker.points[10000]
        )

    def test_add_student_stores_multi_part_last_name(self):
        _, output = self.capture_output(
            self.tracker.add_student,
            "Robert",
            "Jemison Van de Graaff",
            "robertvdgraaff@mit.edu"
        )

        self.assertEqual(["The student has been added."], output)
        self.assertEqual("Robert", self.tracker.students[10000]['Forename'])
        self.assertEqual("Jemison Van de Graaff", self.tracker.students[10000]['Surname'])
        self.assertEqual("robertvdgraaff@mit.edu", self.tracker.students[10000]['Email'])

    def test_add_student_rejects_duplicate_email(self):
        self.tracker.add_student("John", "Doe", "john.doe@example.com")

        _, output = self.capture_output(
            self.tracker.add_student,
            "Jane",
            "Doe",
            "john.doe@example.com"
        )

        self.assertEqual(["This email is already taken."], output)
        self.assertEqual(1, len(self.tracker.students))

    def test_validate_points_accepts_four_non_negative_integers(self):
        result, output = self.capture_output(
            self.tracker.validate_points,
            "10000 10 20 30 40"
        )

        self.assertTrue(result)
        self.assertEqual([], output)

    def test_validate_points_rejects_bad_format(self):
        result, output = self.capture_output(
            self.tracker.validate_points,
            "10000 10 -1 30 40"
        )

        self.assertFalse(result)
        self.assertEqual([], output)

    def test_add_student_points_accumulates_existing_points(self):
        self.tracker.add_student_points([10000, '1', '2', '3', '4'])
        self.tracker.add_student_points(['10000', '10', '20', '30', '40'])

        self.assertEqual(
            {'Python': 11, 'DSA': 22, 'Databases': 33, 'Flask': 44},
            self.tracker.points[10000]
        )

    def test_check_student_exists_returns_true_for_known_student(self):
        self.tracker.add_student("John", "Doe", "john.doe@example.com")

        result, output = self.capture_output(
            self.tracker.check_student_exists,
            "10000"
        )

        self.assertTrue(result)
        self.assertEqual([], output)

    def test_check_student_exists_reports_unknown_student(self):
        result, output = self.capture_output(
            self.tracker.check_student_exists,
            "99999"
        )

        self.assertFalse(result)
        self.assertEqual(["No student is found for id=99999."], output)

    def test_list_student_ids_reports_no_students(self):
        _, output = self.capture_output(self.tracker.list_student_ids)

        self.assertEqual(["No students found."], output)

    def test_list_student_ids_prints_added_student_ids(self):
        self.tracker.add_student("John", "Doe", "john.doe@example.com")
        self.tracker.add_student("Jane", "Doe", "jane.doe@example.com")

        _, output = self.capture_output(self.tracker.list_student_ids)

        self.assertEqual(["Students:", "10000", "10001"], output)

    def test_add_points_updates_existing_student_from_input(self):
        self.tracker.add_student("John", "Doe", "john.doe@example.com")

        with patch('builtins.input', side_effect=["10000 1 2 3 4", "back"]):
            _, output = self.capture_output(self.tracker.add_points)

        self.assertEqual(
            ["Enter an id and points or 'back' to return:", "Points updated."],
            output
        )
        self.assertEqual(
            {'Python': 1, 'DSA': 2, 'Databases': 3, 'Flask': 4},
            self.tracker.points[10000]
        )

    def test_get_student_points_prints_existing_points(self):
        self.tracker.add_student("John", "Doe", "john.doe@example.com")
        self.tracker.add_student_points(["10000", "1", "2", "3", "4"])

        with patch('builtins.input', side_effect=["10000", "back"]):
            _, output = self.capture_output(self.tracker.get_student_points)

        self.assertEqual(
            [
                "Enter an id or 'back' to return:",
                "10000 points: Python=1; DSA=2; Databases=3; Flask=4"
            ],
            output
        )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        sys.argv.pop(1)
        unittest.main()
    else:
        main()
