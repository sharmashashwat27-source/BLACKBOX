# BLACKBOX

BLACKBOX is a Python desktop app for reporting problems around campus.

The idea is simple. Instead of students complaining about the same thing separately, or sending the same message in different group chats, they put the issue in BLACKBOX. Other students can upvote it if they have the same problem.

Admins then see every reported issue in one place, check which ones affect more students, and update them as they are handled.

---

## Important: how to log in

Reviewers and anyone else running this project should **not guess the password**. Login depends on the JSON files shipped with the app.

1. Open `passwords.json` in the project folder.
2. Use a roll number and password **from that file**.
3. The admin password is also in that file (or the default below, if the file does not override it).

`passwords.json` stores student passwords after they are set or changed. If that file is present, **it is the source of truth**. The examples in this README are only the starting scheme. A changed password in `passwords.json` will not match the default pattern.

`blackboxdata.json` stores the issues. It is not the login file. Do not use issue data as a password.

### Default scheme (only if `passwords.json` has not changed that account)

| Role | What to type | Password |
| --- | --- | --- |
| Student | 3-digit roll number, for example `001` | roll number + `123`, so `001` uses `001123` |
| Student | `661` | `661123` |
| Admin | admin login | `admin123` |

Rules that usually cause a failed login:

- The roll number must be **exactly 3 digits**. Use `001`, not `1`.
- Password is case-sensitive.
- If you already changed a password inside the app, the new value is in `passwords.json`. Use that value.
- These passwords are only for this local project. A real app would need proper authentication and password hashing.

If login still fails, open `passwords.json`, copy the password for that roll number exactly, and try again. You do not need to ask for a separate credential list. The JSON file is the credential list.

---

## Features

- Student login using a 3-digit roll number and password
- Guest mode
- Password change for logged-in students
- Report issues with a category, location, and number of students affected
- Search and filter issues
- Upvote existing issues
- Students cannot vote for the same issue more than once
- Automatic priority calculation
- Low, Medium, and High priority levels
- Separate admin dashboard
- Admins can set status to Pending, Under Review, In Progress, Resolved, or Rejected
- Confirmation before deleting rejected issues
- JSON storage so data stays after the app is closed

---

## Priority system

Priority score:

```text
Priority Score = (Reports × 2) + Affected Students + Votes
```

| Score | Priority |
| --- | --- |
| Less than 10 | Low |
| 10 to 24 | Medium |
| 25 or more | High |

An issue becomes more important when more students report it, vote for it, or are affected by it.

---

## Files

| File | What it does |
| --- | --- |
| `main.py` | `User` and `Suggestion` classes, and the priority calculation |
| `bbengine.py` | Adding, saving, loading, ranking, and updating issues |
| `gui.py` | CustomTkinter interface. This is the file you run |
| `blackboxdata.json` | Saved issues. Created or updated by the app |
| `passwords.json` | Student passwords, including any password a student changed. **Check this file before logging in** |
| `README.md` | This file |

You are expected to use the JSON files already in the project folder. Do not delete `passwords.json` or `blackboxdata.json` if you want the shipped accounts and issues. If `passwords.json` is missing, the app falls back to the default `roll + 123` scheme.

---

## Running the project

Install CustomTkinter:

```bash
pip install customtkinter
```

Run the app from the project folder (the same folder as the JSON files):

```bash
python gui.py
```

Then:

1. Open `passwords.json`.
2. Log in as a student with a roll number and the matching password from that file.
3. Or log in as admin with the admin password from that file, otherwise `admin123`.

---

## Why BLACKBOX?

Campus problems get lost in group chats. Several people can have the same complaint, and nobody can see how many people are affected.

BLACKBOX gives students one place to report a problem and support an existing report. It gives admins a clearer view of which issues are getting the most attention.

It turns the usual "someone should tell the admin" situation into a system where someone can report it and have it tracked.

BLACKBOX is built with Python, CustomTkinter, JSON, and object-oriented programming.
