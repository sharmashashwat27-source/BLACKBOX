BLACKBOX

BLACKBOX is a Python desktop app for reporting problems around campus.

The idea is pretty simple. Instead of students complaining about the same thing separately or sending messages in different group chats, they can put the issue in BLACKBOX and let other students upvote it if they have the same problem.

Admins can then see the reported issues in one place, check which ones are affecting more students, and update them as they are handled.

Features

Student login using a 3-digit roll number and password

Guest mode

Password change for logged-in students

Report issues with a category, location, and number of students affected

Search and filter issues

Upvote existing issues

Students cannot vote for the same issue more than once

Automatic priority calculation

Low, Medium, and High priority levels

Separate admin dashboard

Admins can update issue status between Pending, Under Review, In Progress, Resolved, and Rejected

Confirmation before deleting rejected issues

JSON storage so the data stays after closing the app

Priority System

The priority score is calculated using:

Priority Score = (Reports × 2) + Affected Students + Votes

Less than 10 is Low priority.

10 to 24 is Medium priority.

25 or more is High priority.

This means an issue can become more important when more students report it, vote for it, or are affected by it.

Files

BLACKBOX contains main.py, bbengine.py, gui.py, blackboxdata.json, passwords.json, and README.md.

main.py contains the User and Suggestion classes and the priority calculation.

bbengine.py handles adding, saving, loading, ranking, and updating issues.

gui.py contains the CustomTkinter interface.

blackboxdata.json stores the issue data.

passwords.json stores changed student passwords.

Running the project

First install CustomTkinter using:

pip install customtkinter

Then run:

python gui.py

The default student login is roll number 001 with password 001123.

For example, roll number 661 uses password 661123.

The admin password is admin123.

These passwords are only for this local project. A real application would need proper authentication and password hashing.

Why BLACKBOX?

Campus problems can easily get lost in group chats. Sometimes multiple people have the exact same complaint, but nobody really knows how many people are affected.

BLACKBOX gives students one place to report problems and support existing reports. It also gives admins a clearer idea of which issues are getting the most attention.

I made BLACKBOX to turn the usual "someone should tell the admin" situation into an actual system where someone can just report it and get it tracked.

BLACKBOX is built using Python, CustomTkinter, JSON, and object-oriented programming.
