BLACKBOX
BLACKBOX is a Python desktop app made to make campus complaints less chaotic.

Instead of students repeatedly complaining about the same thing separately, they can report an issue, upvote existing reports, and let the most important problems rise to the top. Admins get a priority-based dashboard where they can review issues, update their status, and handle them properly.

The idea is simple: make student feedback visible, organised, and easier to act on.

Features
Student login using a 3-digit roll number and password

Guest mode option

Password change feature for logged-in students

Report campus issues with category, location, and affected-student count

Search and filter submitted issues

Upvote issues

Prevent duplicate votes from the same student

Automatic priority calculation

Low, Medium, and High priority labels

Separate admin dashboard

Admin status updates: Pending, Under Review, In Progress, Resolved, and Rejected

Confirmation before deleting rejected issues

JSON file storage so data remains after restarting the app

Priority system
Issues are ranked using the following formula:

text
Priority Score = (Reports × 2) + Affected Students + Votes
Score	Priority
Less than 10	LOW
10 to 24	MEDIUM
25 or above	HIGH
This means issues with more reports, votes, and affected students appear higher on the admin dashboard.

Files
text
BLACKBOX/
├── main.py
├── bbengine.py
├── gui.py
├── blackboxdata.json
├── passwords.json
└── README.md
main.py contains the user and suggestion classes, including priority calculations.

bbengine.py handles adding, saving, loading, ranking, and updating issues.

gui.py contains the CustomTkinter interface.

blackboxdata.json stores issue data.

passwords.json stores changed student passwords.

Running the project
Install CustomTkinter:

bash
pip install customtkinter
Then run:

bash
python gui.py
Default student login format:

text
Roll Number: 001
Password: 001123
For example, roll number 661 uses password 661123.

Admin password:

text
admin123
These passwords are only for this local academic project. A real application should use secure authentication and password hashing.

Why BLACKBOX?
Campus issues often get lost in group chats or are repeated by different students. BLACKBOX puts everything in one place, lets students support existing reports, and helps admins notice which problems need attention first.

The project uses Python, CustomTkinter, JSON storage, and object-oriented programming to create a simple but functional campus issue tracker.
