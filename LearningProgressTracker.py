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
        print("Unknown command!")

def main():
    tracker = LearningProgressTracker()
    tracker.run()

if __name__ == '__main__':
    main()

