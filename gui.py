# Import JSON support for saving and loading changed passwords.
import json

# Import CustomTkinter for the full application interface.
import customtkinter as ctk

# Import Tkinter popups for confirmations and success messages.
from tkinter import messagebox

# Import the JSON storage and priority-management backend.
from bbengine import Priority_Engine


# ===== UI REDESIGN CHANGE =====
# Keep all colours in one place for a simple, consistent dark aesthetic.
APP_BG = "#0F172A"
PANEL_BG = "#172033"
CARD_BG = "#202B3D"
INPUT_BG = "#273449"
BORDER = "#334155"

PRIMARY = "#3B82F6"
PRIMARY_HOVER = "#2563EB"

TEXT = "#F8FAFC"
MUTED_TEXT = "#94A3B8"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"
PURPLE = "#A855F7"


# Configure CustomTkinter's default display mode and built-in palette.
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# Create the main BLACKBOX desktop application.
class GUI(ctk.CTk):

    # Create the main window and initialise app state.
    def __init__(self):
        super().__init__()

        # ===== UI REDESIGN CHANGE =====
        # Use a clean dark navy application background.
        self.configure(fg_color=APP_BG)
        self.title("BLACKBOX | Campus Feedback")
        self.geometry("900x680")
        self.minsize(820, 620)

        # Create the backend engine that loads/saves issue data.
        self.engine = Priority_Engine()

        # Store basic application user state.
        self.ADMIN_PASSWORD = "admin123"
        self.current_user = "guest_student"
        self.student_user = "guest_student"

        # Load custom student passwords if any exist.
        self.user_passwords = self.load_passwords()

        # Open the roll-number login dialog when the app starts.
        self.login_student()

    # Load saved student passwords from a JSON file.
    def load_passwords(self):
        try:
            with open("passwords.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # Save custom student passwords into a JSON file.
    def save_passwords(self):
        with open("passwords.json", "w", encoding="utf-8") as file:
            json.dump(self.user_passwords, file, indent=4)

    # Ask the user to log in as a student or continue as a guest.
    def login_student(self):
        # Ask for the three-digit roll number.
        dialog = ctk.CTkInputDialog(
            text=(
                "Enter your 3-digit Roll Number (example: 001)\n\n"
                "Press Cancel to continue as a guest."
            ),
            title="Student Login"
        )
        roll_number = dialog.get_input()

        # Use guest mode when no roll number is supplied.
        if roll_number is None or not roll_number.strip():
            self.current_user = "guest_student"
            self.student_user = "guest_student"
            self.setup_ui()
            return

        # Remove accidental spaces from the roll number.
        roll_number = roll_number.strip()

        # Require exactly three digits.
        if len(roll_number) != 3 or not roll_number.isdigit():
            messagebox.showerror(
                "Invalid Roll Number",
                "Enter exactly 3 digits, for example: 001."
            )
            self.login_student()
            return

        # Ask for the corresponding student password.
        password_dialog = ctk.CTkInputDialog(
            text="Enter password:",
            title="Student Login"
        )
        password = password_dialog.get_input()

        # Fall back to guest mode if password entry is cancelled.
        if password is None:
            self.current_user = "guest_student"
            self.student_user = "guest_student"
            self.setup_ui()
            return

        # Check a saved password, or use the default rollnumber123 password.
        password = password.strip()
        user_key = f"student_{roll_number}"
        expected_password = self.user_passwords.get(
            user_key,
            f"{roll_number}123"
        )

        # Log in as a guest if the password is invalid.
        if password != expected_password:
            messagebox.showerror(
                "Invalid Password",
                "Login failed. Continuing in Guest Mode."
            )
            self.current_user = "guest_student"
            self.student_user = "guest_student"

        # Log in as the authenticated student.
        else:
            self.current_user = user_key
            self.student_user = user_key
            messagebox.showinfo("Welcome", "Logged in successfully.")

        # Build the main interface after the login attempt.
        self.setup_ui()

    # Let an authenticated student change their own password.
    def change_password(self):
        # Do not permit password changes from guest mode.
        if self.current_user == "guest_student":
            messagebox.showwarning(
                "Guest Mode",
                "Guests cannot change passwords."
            )
            return

        # Ask for the currently active password.
        current_dialog = ctk.CTkInputDialog(
            text="Enter your current password:",
            title="Security Check"
        )
        current_password = current_dialog.get_input()

        # Stop if the dialog is cancelled.
        if current_password is None:
            return

        # Find the active password for the logged-in student.
        roll_number = self.current_user.replace("student_", "")
        active_password = self.user_passwords.get(
            self.current_user,
            f"{roll_number}123"
        )

        # Stop when the old password is incorrect.
        if current_password.strip() != active_password:
            messagebox.showerror(
                "Incorrect Password",
                "The current password is incorrect."
            )
            return

        # Ask for the student's new password.
        new_dialog = ctk.CTkInputDialog(
            text="Enter a new password:",
            title="Change Password"
        )
        new_password = new_dialog.get_input()

        # Stop if the new-password prompt is cancelled.
        if new_password is None:
            return

        # Validate the new password length.
        new_password = new_password.strip()

        if len(new_password) < 4:
            messagebox.showerror(
                "Invalid Password",
                "The new password must have at least 4 characters."
            )
            return

        # Save the student's replacement password.
        self.user_passwords[self.current_user] = new_password
        self.save_passwords()

        messagebox.showinfo(
            "Password Changed",
            "Your password was updated successfully."
        )

    # Build the full main application frame, header, and default view.
    def setup_ui(self):
        # Remove every old widget when rebuilding the layout.
        for widget in self.winfo_children():
            widget.destroy()

        # ===== UI REDESIGN CHANGE =====
        # Add a minimal branded header instead of a plain top bar.
        header = ctk.CTkFrame(
            self,
            fg_color=PANEL_BG,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )
        header.pack(fill="x", padx=24, pady=(20, 12))

        # ===== UI REDESIGN CHANGE =====
        # Create a compact brand block with a title and subtitle.
        brand_frame = ctk.CTkFrame(header, fg_color="transparent")
        brand_frame.pack(side="left", padx=18, pady=14)

        ctk.CTkLabel(
            brand_frame,
            text="BLACKBOX",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_frame,
            text="Campus feedback platform",
            font=ctk.CTkFont(size=11),
            text_color=MUTED_TEXT
        ).pack(anchor="w", pady=(1, 0))

        # ===== UI REDESIGN CHANGE =====
        # Create a neat account label on the header's right side.
        account_frame = ctk.CTkFrame(
            header,
            fg_color=CARD_BG,
            corner_radius=10
        )
        account_frame.pack(side="right", padx=(8, 18), pady=14)

        self.user_label = ctk.CTkLabel(
            account_frame,
            text=self.display_user_name(),
            font=ctk.CTkFont(size=12),
            text_color=TEXT
        )
        self.user_label.pack(side="left", padx=(12, 8), pady=8)

        # Let authenticated students open their password-change dialog.
        if self.current_user.startswith("student_"):
            ctk.CTkButton(
                account_frame,
                text="Password",
                width=82,
                height=28,
                fg_color="#334155",
                hover_color="#475569",
                font=ctk.CTkFont(size=11),
                command=self.change_password
            ).pack(side="left", padx=(0, 6), pady=6)

        # Let users switch between student and administrator views.
        self.role_optionmenu = ctk.CTkOptionMenu(
            account_frame,
            values=["Student", "Admin"],
            width=105,
            height=28,
            fg_color=PRIMARY,
            button_color=PRIMARY_HOVER,
            button_hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(size=11),
            command=self.switch_view
        )
        self.role_optionmenu.set(
            "Admin" if self.current_user == "admin" else "Student"
        )
        self.role_optionmenu.pack(side="left", padx=(0, 6), pady=6)

        # ===== UI REDESIGN CHANGE =====
        # Use one spacious central panel for both dashboards.
        self.container = ctk.CTkFrame(
            self,
            fg_color=PANEL_BG,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )
        self.container.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 24)
        )

        # Show the student interface first.
        self.show_student_view()

    # Format the active account name for display in the header.
    def display_user_name(self):
        if self.current_user == "admin":
            return "Admin"

        if self.current_user == "guest_student":
            return "Guest student"

        roll_number = self.current_user.replace("student_", "")
        return f"Student {roll_number}"

    # Refresh the account label after switching user roles.
    def refresh_header_label(self):
        if hasattr(self, "user_label"):
            self.user_label.configure(text=self.display_user_name())

    # Switch the interface between Student and Admin mode.
    def switch_view(self, role):
        # Ask for the admin password before granting admin access.
        if role == "Admin":
            dialog = ctk.CTkInputDialog(
                text="Enter admin password:",
                title="Admin Verification"
            )
            password = dialog.get_input()

            # Restore Student mode when authentication fails.
            if password != self.ADMIN_PASSWORD:
                messagebox.showerror(
                    "Access Denied",
                    "Incorrect admin password."
                )
                self.role_optionmenu.set("Student")
                return

            # Mark the current user as an administrator.
            self.current_user = "admin"

        # Restore the logged-in student identity when leaving Admin mode.
        else:
            self.current_user = self.student_user

        # Refresh the header and page content without asking again.
        self.refresh_header_label()
        self.render_current_view(role)

    # Remove current page widgets and render the selected role page.
    def render_current_view(self, role=None):
        # Infer the current role if no role is supplied.
        if role is None:
            role = "Admin" if self.current_user == "admin" else "Student"

        # Clear the existing dashboard contents.
        for widget in self.container.winfo_children():
            widget.destroy()

        # Draw the requested page.
        if role == "Admin":
            self.show_admin_view()
        else:
            self.show_student_view()

    # Return an icon for each supported issue category.
    def get_category_icon(self, category):
        category_icons = {
            "Facilities": "🔧",
            "Safety": "🛡",
            "Communication": "📢",
            "Campus": "🏫",
            "Other": "💬"
        }
        return category_icons.get(category, "•")

    # Return a colour representing a workflow status.
    def get_status_color(self, status):
        status_colors = {
            "Pending": WARNING,
            "Under Review": PRIMARY,
            "In Progress": PURPLE,
            "Resolved": SUCCESS,
            "Rejected": DANGER
        }
        return status_colors.get(status, MUTED_TEXT)

    # Return a colour representing the current calculated priority.
    def get_priority_color(self, priority_level):
        priority_colors = {
            "HIGH": DANGER,
            "MEDIUM": WARNING,
            "LOW": SUCCESS
        }
        return priority_colors.get(priority_level, MUTED_TEXT)

    # Build the simple student issue browsing page.
    def show_student_view(self):
        # ===== UI REDESIGN CHANGE =====
        # Add a concise page heading and a single primary action.
        top_bar = ctk.CTkFrame(self.container, fg_color="transparent")
        top_bar.pack(fill="x", padx=22, pady=(20, 10))

        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="Campus issues",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Raise an issue or support a report from another student.",
            font=ctk.CTkFont(size=12),
            text_color=MUTED_TEXT
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkButton(
            top_bar,
            text="+ Report issue",
            width=135,
            height=36,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.open_add_dialog
        ).pack(side="right", pady=4)

        # ===== UI REDESIGN CHANGE =====
        # Put search on its own clean row, with filters underneath.
        search_entry = ctk.CTkEntry(
            self.container,
            placeholder_text="Search by issue, category, location, or status...",
            height=38,
            fg_color=INPUT_BG,
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text_color=MUTED_TEXT
        )
        search_entry.pack(fill="x", padx=22, pady=(4, 8))

        filters = ctk.CTkFrame(self.container, fg_color="transparent")
        filters.pack(fill="x", padx=22, pady=(0, 10))

        category_menu = ctk.CTkOptionMenu(
            filters,
            values=[
                "All",
                "Facilities",
                "Safety",
                "Communication",
                "Campus",
                "Other"
            ],
            width=150,
            height=32,
            fg_color=INPUT_BG,
            button_color="#334155",
            button_hover_color="#475569"
        )
        category_menu.set("All")
        category_menu.pack(side="left", padx=(0, 8))

        status_menu = ctk.CTkOptionMenu(
            filters,
            values=[
                "All",
                "Pending",
                "Under Review",
                "In Progress",
                "Resolved"
            ],
            width=150,
            height=32,
            fg_color=INPUT_BG,
            button_color="#334155",
            button_hover_color="#475569"
        )
        status_menu.set("All")
        status_menu.pack(side="left")

        # Create the holder for the scrollable list of issue cards.
        list_holder = ctk.CTkFrame(self.container, fg_color="transparent")
        list_holder.pack(fill="both", expand=True, padx=22, pady=(0, 20))

        # Redraw issue cards when a search/filter option changes.
        def draw_list(*_args):
            # Remove the old scroll list before rebuilding it.
            for widget in list_holder.winfo_children():
                widget.destroy()

            # Create a scrollable holder for issue cards.
            scroll_frame = ctk.CTkScrollableFrame(
                list_holder,
                fg_color="transparent"
            )
            scroll_frame.pack(fill="both", expand=True)

            # Read the active search and filter values.
            query = search_entry.get().strip().lower()
            selected_category = category_menu.get()
            selected_status = status_menu.get()

            # Build a list of all matching issues.
            matching_issues = []

            for issue in self.engine.get_ranked_suggestions():
                if (
                    selected_category != "All"
                    and issue.category != selected_category
                ):
                    continue

                if (
                    selected_status != "All"
                    and issue.status.lower() != selected_status.lower()
                ):
                    continue

                searchable_text = (
                    f"{issue.suggestion_id} "
                    f"{issue.text} "
                    f"{issue.location} "
                    f"{issue.category} "
                    f"{issue.status}"
                ).lower()

                if query and query not in searchable_text:
                    continue

                matching_issues.append(issue)

            # Display a quiet empty-state message when nothing matches.
            if not matching_issues:
                ctk.CTkLabel(
                    scroll_frame,
                    text="No issues match your search.",
                    font=ctk.CTkFont(size=14),
                    text_color=MUTED_TEXT
                ).pack(pady=45)
                return

            # Draw one simple card for each matching issue.
            for issue in matching_issues:
                self.create_student_issue_card(scroll_frame, issue)

        # Refresh issue cards when the user interacts with filters.
        search_entry.bind("<KeyRelease>", draw_list)
        category_menu.configure(command=draw_list)
        status_menu.configure(command=draw_list)

        # Draw the initial student list.
        draw_list()

    # Create one compact aesthetic issue card for the student view.
    def create_student_issue_card(self, parent, issue):
        # Calculate card display values.
        priority_level = issue.calc_priority_level()
        priority_color = self.get_priority_color(priority_level)
        status_color = self.get_status_color(issue.status)

        # Determine if the logged-in user already voted for this issue.
        upvoted_by = getattr(issue, "upvoted_by", []) or []
        has_voted = self.current_user in upvoted_by

        # ===== UI REDESIGN CHANGE =====
        # Create a clean card with a subtle priority stripe on the left.
        card = ctk.CTkFrame(
            parent,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )
        card.pack(fill="x", pady=6, padx=2)

        priority_strip = ctk.CTkFrame(
            card,
            width=5,
            fg_color=priority_color,
            corner_radius=3
        )
        priority_strip.pack(side="left", fill="y", padx=(0, 12), pady=10)

        # Create the main issue information section.
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8),
            pady=12
        )

        # Make category and issue title easy to scan.
        ctk.CTkLabel(
            info_frame,
            text=f"{self.get_category_icon(issue.category)}  {issue.category}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=PRIMARY
        ).pack(anchor="w")

        description = issue.text
        if len(description) > 72:
            description = description[:72] + "..."

        ctk.CTkLabel(
            info_frame,
            text=description,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT,
            anchor="w",
            justify="left",
            wraplength=470
        ).pack(anchor="w", pady=(3, 4))

        # Display concise metadata under the title.
        ctk.CTkLabel(
            info_frame,
            text=(
                f"{issue.location}  •  "
                f"{issue.affected} affected  •  "
                f"{issue.votes} votes"
            ),
            font=ctk.CTkFont(size=11),
            text_color=MUTED_TEXT
        ).pack(anchor="w")

        # Create a right-side section for the status and upvote action.
        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.pack(side="right", padx=12, pady=12)

        # ===== UI REDESIGN CHANGE =====
        # Show status as a small coloured pill rather than inline text.
        ctk.CTkLabel(
            action_frame,
            text=f" {issue.status} ",
            fg_color=status_color,
            text_color="#FFFFFF",
            corner_radius=8,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="e", pady=(0, 8))

        # Create a compact vote action.
        ctk.CTkButton(
            action_frame,
            text="Voted" if has_voted else f"▲ {issue.votes}",
            width=82,
            height=30,
            fg_color="#334155" if has_voted else PRIMARY,
            hover_color="#475569" if has_voted else PRIMARY_HOVER,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda issue_id=issue.suggestion_id: self.vote_issue(
                issue_id
            )
        ).pack(anchor="e")

    # Record an upvote while preventing duplicate votes.
    def vote_issue(self, issue_id):
        # Require a student account before voting.
        if self.current_user == "guest_student":
            messagebox.showwarning(
                "Login Required",
                "Log in with a roll number to upvote an issue."
            )
            return

        # Find the selected issue.
        for issue in self.engine.suggestions:
            if issue.suggestion_id == issue_id:
                # Create an upvoter list for older saved issues.
                if not hasattr(issue, "upvoted_by"):
                    issue.upvoted_by = []

                # Block a second vote from the same student.
                if self.current_user in issue.upvoted_by:
                    messagebox.showwarning(
                        "Already Voted",
                        "You have already upvoted this issue."
                    )
                    return

                # Save the vote and redraw the student dashboard.
                issue.votes += 1
                issue.upvoted_by.append(self.current_user)
                self.engine.save_suggestion()

                self.render_current_view("Student")
                return

        # Inform the user when an issue cannot be found.
        messagebox.showerror("Issue Not Found", "This issue no longer exists.")

    # Open a cleaner form popup for creating a new campus issue.
    def open_add_dialog(self):
        # Require authenticated students to submit issues.
        if self.current_user == "guest_student":
            messagebox.showwarning(
                "Login Required",
                "Log in with a roll number to report an issue."
            )
            return

        # ===== UI REDESIGN CHANGE =====
        # Create a smaller, structured popup instead of an empty tall form.
        dialog = ctk.CTkToplevel(self)
        dialog.title("Report an Issue")
        dialog.geometry("470x560")
        dialog.resizable(False, False)
        dialog.configure(fg_color=PANEL_BG)
        dialog.transient(self)
        dialog.grab_set()
        dialog.focus_force()

        # Create a form wrapper with consistent spacing.
        form = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )
        form.pack(fill="both", expand=True, padx=32, pady=28)

        # Display form heading and short helper text.
        ctk.CTkLabel(
            form,
            text="Report an issue",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            form,
            text="Share a campus problem so it can be reviewed.",
            font=ctk.CTkFont(size=12),
            text_color=MUTED_TEXT
        ).pack(anchor="w", pady=(3, 20))

        # Add the description field label.
        ctk.CTkLabel(
            form,
            text="Issue description",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", pady=(0, 5))

        # ===== UI REDESIGN CHANGE =====
        # Use a multiline box so students can write proper descriptions.
        description_box = ctk.CTkTextbox(
            form,
            width=400,
            height=105,
            fg_color=INPUT_BG,
            border_color=BORDER,
            border_width=1,
            text_color=TEXT,
            corner_radius=8
        )
        description_box.pack(fill="x", pady=(0, 14))

        # Create a two-column row for category and location.
        two_column_frame = ctk.CTkFrame(form, fg_color="transparent")
        two_column_frame.pack(fill="x", pady=(0, 14))

        # Create the category input column.
        category_column = ctk.CTkFrame(two_column_frame, fg_color="transparent")
        category_column.pack(side="left", fill="x", expand=True, padx=(0, 7))

        ctk.CTkLabel(
            category_column,
            text="Category",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", pady=(0, 5))

        category_menu = ctk.CTkOptionMenu(
            category_column,
            values=[
                "Facilities",
                "Safety",
                "Communication",
                "Campus",
                "Other"
            ],
            height=38,
            fg_color=INPUT_BG,
            button_color="#334155",
            button_hover_color="#475569"
        )
        category_menu.set("Facilities")
        category_menu.pack(fill="x")

        # Create the location input column.
        location_column = ctk.CTkFrame(two_column_frame, fg_color="transparent")
        location_column.pack(side="left", fill="x", expand=True, padx=(7, 0))

        ctk.CTkLabel(
            location_column,
            text="Location",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", pady=(0, 5))

        location_entry = ctk.CTkEntry(
            location_column,
            placeholder_text="Example: Library",
            height=38,
            fg_color=INPUT_BG,
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text_color=MUTED_TEXT
        )
        location_entry.pack(fill="x")

        # Add the estimated affected students input label.
        ctk.CTkLabel(
            form,
            text="Estimated students affected",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", pady=(0, 5))

        affected_entry = ctk.CTkEntry(
            form,
            placeholder_text="Enter a number from 1 to 60",
            height=38,
            fg_color=INPUT_BG,
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text_color=MUTED_TEXT
        )
        affected_entry.pack(fill="x")

        # Show validation problems directly in the form.
        error_label = ctk.CTkLabel(
            form,
            text="",
            text_color=DANGER,
            font=ctk.CTkFont(size=11),
            wraplength=400,
            justify="left"
        )
        error_label.pack(anchor="w", pady=(6, 0))

        # Display an inline validation error.
        def show_error(message):
            error_label.configure(text=message)

        # Clear old validation errors while the student edits fields.
        def clear_error(*_args):
            error_label.configure(text="")

        # Validate all inputs and submit the issue.
        def save_and_close():
            # Get cleaned values from all form inputs.
            text = description_box.get("1.0", "end").strip()
            category = category_menu.get().strip()
            location = location_entry.get().strip()
            affected_text = affected_entry.get().strip()

            # Require a description, category, location, and affected count.
            if not text or not category or not location or not affected_text:
                show_error("Please complete all fields before submitting.")
                return

            # Require the affected value to be a whole number.
            if not affected_text.isdigit():
                show_error("Students affected must be a whole number.")
                return

            # Convert the validated affected value into an integer.
            affected = int(affected_text)

            # Keep affected count within the project limits.
            if not 1 <= affected <= 60:
                show_error("Students affected must be between 1 and 60.")
                return

            # Create and save the suggestion through the backend engine.
            result = self.engine.add_suggestion(
                text=text,
                category=category,
                location=location,
                affected=affected
            )

            # Close the form and refresh the issue list.
            dialog.destroy()
            messagebox.showinfo("Issue Submitted", result)
            self.render_current_view("Student")

        # ===== UI REDESIGN CHANGE =====
        # Add a simple footer with secondary Cancel and primary Submit actions.
        button_frame = ctk.CTkFrame(form, fg_color="transparent")
        button_frame.pack(fill="x", pady=(22, 0))

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            height=38,
            fg_color="#334155",
            hover_color="#475569",
            command=dialog.destroy
        ).pack(side="left")

        ctk.CTkButton(
            button_frame,
            text="Submit report",
            width=170,
            height=38,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=save_and_close
        ).pack(side="right")

        # Clear errors as the user corrects form values.
        description_box.bind("<KeyRelease>", clear_error)
        location_entry.bind("<KeyRelease>", clear_error)
        affected_entry.bind("<KeyRelease>", clear_error)
        category_menu.configure(command=clear_error)

        # Put the cursor in the description box on popup opening.
        description_box.focus()

    # Open the admin popup for changing one issue's workflow status.
    def change_status(self, issue_id):
        # Ensure only an active admin can alter issue statuses.
        if self.current_user != "admin":
            messagebox.showerror(
                "Access Denied",
                "Only the admin can change issue statuses."
            )
            return

        # Define the allowed status changes.
        statuses = [
            "Pending",
            "Under Review",
            "In Progress",
            "Resolved",
            "Rejected"
        ]

        # Find the selected issue object.
        issue = None

        for suggestion in self.engine.suggestions:
            if suggestion.suggestion_id == issue_id:
                issue = suggestion
                break

        # Stop if the selected issue no longer exists.
        if issue is None:
            messagebox.showerror("Issue Not Found", "This issue no longer exists.")
            return

        # Create the status selection popup.
        dialog = ctk.CTkToplevel(self)
        dialog.title("Change Status")
        dialog.geometry("360x280")
        dialog.resizable(False, False)
        dialog.configure(fg_color=PANEL_BG)
        dialog.transient(self)
        dialog.grab_set()

        # Display the selected issue reference.
        ctk.CTkLabel(
            dialog,
            text=f"Update issue #{issue_id}",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=TEXT
        ).pack(pady=(28, 5))

        ctk.CTkLabel(
            dialog,
            text="Choose the current workflow status.",
            font=ctk.CTkFont(size=12),
            text_color=MUTED_TEXT
        ).pack(pady=(0, 20))

        # Let the admin choose one valid status.
        status_menu = ctk.CTkOptionMenu(
            dialog,
            values=statuses,
            width=260,
            height=38,
            fg_color=INPUT_BG,
            button_color="#334155",
            button_hover_color="#475569"
        )
        status_menu.set(issue.status)
        status_menu.pack(pady=8)

        # Save the chosen status using exactly one backend update call.
        def save_status():
            # Read the new status selection.
            new_status = status_menu.get()

            # Confirm destructive removal when rejecting an issue.
            if new_status == "Rejected":
                should_delete = messagebox.askyesno(
                    "Reject and Delete",
                    (
                        f"Rejecting issue #{issue_id} will permanently "
                        "delete it.\n\nContinue?"
                    ),
                    parent=dialog
                )

                if not should_delete:
                    return

            # Update the status or delete the rejected issue.
            success, result_message = self.engine.update_status(
                issue_id,
                new_status
            )

            # Close and refresh without triggering the admin password again.
            if success:
                dialog.destroy()
                messagebox.showinfo("Status Updated", result_message)
                self.render_current_view("Admin")

            # Keep the popup open and show backend errors when needed.
            else:
                messagebox.showerror(
                    "Error",
                    result_message,
                    parent=dialog
                )

        # Create the final save-status action button.
        ctk.CTkButton(
            dialog,
            text="Save changes",
            width=260,
            height=38,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=save_status
        ).pack(pady=(20, 10))

    # Build the streamlined admin issue-management dashboard.
    def show_admin_view(self):
        # ===== UI REDESIGN CHANGE =====
        # Add a simple heading with lightweight dashboard context.
        top_bar = ctk.CTkFrame(self.container, fg_color="transparent")
        top_bar.pack(fill="x", padx=22, pady=(20, 10))

        ctk.CTkLabel(
            top_bar,
            text="Admin dashboard",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            top_bar,
            text="Review, prioritise, and update campus issues.",
            font=ctk.CTkFont(size=12),
            text_color=MUTED_TEXT
        ).pack(anchor="w", pady=(2, 0))

        # ===== UI REDESIGN CHANGE =====
        # Show four minimal statistics cards instead of heavy analytics.
        all_issues = self.engine.suggestions
        total_issues = len(all_issues)

        high_priority_count = sum(
            issue.calc_priority_level() == "HIGH"
            for issue in all_issues
        )

        pending_count = sum(
            issue.status == "Pending"
            for issue in all_issues
        )

        resolved_count = sum(
            issue.status == "Resolved"
            for issue in all_issues
        )

        stats_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        stats_frame.pack(fill="x", padx=22, pady=(2, 14))

        self.create_stat_card(
            stats_frame,
            "Total issues",
            total_issues,
            PRIMARY
        )
        self.create_stat_card(
            stats_frame,
            "High priority",
            high_priority_count,
            DANGER
        )
        self.create_stat_card(
            stats_frame,
            "Pending",
            pending_count,
            WARNING
        )
        self.create_stat_card(
            stats_frame,
            "Resolved",
            resolved_count,
            SUCCESS
        )

        # Create the admin search/filter row.
        filter_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        filter_frame.pack(fill="x", padx=22, pady=(0, 10))

        search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Search issues...",
            width=220,
            height=36,
            fg_color=INPUT_BG,
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text_color=MUTED_TEXT
        )
        search_entry.pack(side="left", padx=(0, 8))

        category_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=[
                "All",
                "Facilities",
                "Safety",
                "Communication",
                "Campus",
                "Other"
            ],
            width=128,
            height=36,
            fg_color=INPUT_BG,
            button_color="#334155",
            button_hover_color="#475569"
        )
        category_menu.set("All")
        category_menu.pack(side="left", padx=4)

        status_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=[
                "All",
                "Pending",
                "Under Review",
                "In Progress",
                "Resolved"
            ],
            width=128,
            height=36,
            fg_color=INPUT_BG,
            button_color="#334155",
            button_hover_color="#475569"
        )
        status_menu.set("All")
        status_menu.pack(side="left", padx=4)

        priority_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "LOW", "MEDIUM", "HIGH"],
            width=108,
            height=36,
            fg_color=INPUT_BG,
            button_color="#334155",
            button_hover_color="#475569"
        )
        priority_menu.set("All")
        priority_menu.pack(side="left", padx=4)

        # Create the holder for the admin issue list.
        list_holder = ctk.CTkFrame(self.container, fg_color="transparent")
        list_holder.pack(fill="both", expand=True, padx=22, pady=(0, 20))

        # Redraw the admin issue list after filters change.
        def draw_admin_list(*_args):
            # Clear all old list widgets.
            for widget in list_holder.winfo_children():
                widget.destroy()

            # Create a scrollable list container.
            scroll_frame = ctk.CTkScrollableFrame(
                list_holder,
                fg_color="transparent"
            )
            scroll_frame.pack(fill="both", expand=True)

            # Read selected filter values.
            query = search_entry.get()
            category = category_menu.get()
            status = status_menu.get()
            priority = priority_menu.get()

            # Filter by query, category, and status.
            suggestions = self.get_filtered_suggestions(
                query,
                category,
                status
            )

            # Filter by calculated priority when selected.
            if priority != "All":
                suggestions = [
                    issue for issue in suggestions
                    if issue.calc_priority_level() == priority
                ]

            # Display an empty state for no matching admin records.
            if not suggestions:
                ctk.CTkLabel(
                    scroll_frame,
                    text="No issues match the selected filters.",
                    font=ctk.CTkFont(size=14),
                    text_color=MUTED_TEXT
                ).pack(pady=45)
                return

            # Build one admin issue card per matching issue.
            for issue in suggestions:
                self.create_admin_issue_card(scroll_frame, issue)

        # Refresh the admin issue list when filters are changed.
        search_entry.bind("<KeyRelease>", draw_admin_list)
        category_menu.configure(command=draw_admin_list)
        status_menu.configure(command=draw_admin_list)
        priority_menu.configure(command=draw_admin_list)

        # Draw the initial admin list.
        draw_admin_list()

    # Build a reusable small statistic card for the admin dashboard.
    def create_stat_card(self, parent, title, value, color):
        # Create the visual stat card.
        card = ctk.CTkFrame(
            parent,
            fg_color=CARD_BG,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )
        card.pack(side="left", fill="x", expand=True, padx=4)

        # Display the stat label.
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color=MUTED_TEXT
        ).pack(pady=(10, 0))

        # Display the coloured stat number.
        ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=color
        ).pack(pady=(0, 10))

    # Create one admin card with score, priority, and status controls.
    def create_admin_issue_card(self, parent, issue):
        # Calculate priority display values.
        priority_level = issue.calc_priority_level()
        priority_score = issue.calc_priority_score()
        priority_color = self.get_priority_color(priority_level)
        status_color = self.get_status_color(issue.status)

        # ===== UI REDESIGN CHANGE =====
        # Use the same simple card style for visual consistency.
        card = ctk.CTkFrame(
            parent,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )
        card.pack(fill="x", pady=6, padx=2)

        priority_strip = ctk.CTkFrame(
            card,
            width=5,
            fg_color=priority_color,
            corner_radius=3
        )
        priority_strip.pack(side="left", fill="y", padx=(0, 12), pady=10)

        # Create the primary issue details section.
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8),
            pady=12
        )

        # Display the issue category and ID.
        ctk.CTkLabel(
            info_frame,
            text=(
                f"#{issue.suggestion_id}  "
                f"{self.get_category_icon(issue.category)}  "
                f"{issue.category}"
            ),
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=PRIMARY
        ).pack(anchor="w")

        # Display a shortened issue description.
        description = issue.text
        if len(description) > 78:
            description = description[:78] + "..."

        ctk.CTkLabel(
            info_frame,
            text=description,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT,
            wraplength=455,
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(3, 4))

        # Display admin-relevant metadata and the calculated score.
        ctk.CTkLabel(
            info_frame,
            text=(
                f"{issue.location}  •  "
                f"{issue.affected} affected  •  "
                f"{issue.votes} votes  •  "
                f"Score {priority_score}"
            ),
            font=ctk.CTkFont(size=11),
            text_color=MUTED_TEXT
        ).pack(anchor="w")

        # Display priority as a concise label.
        ctk.CTkLabel(
            info_frame,
            text=f"{priority_level} PRIORITY",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=priority_color
        ).pack(anchor="w", pady=(5, 0))

        # Create right-side admin controls.
        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.pack(side="right", padx=12, pady=12)

        # Display the current workflow status.
        ctk.CTkLabel(
            action_frame,
            text=f" {issue.status} ",
            fg_color=status_color,
            text_color="#FFFFFF",
            corner_radius=8,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="e", pady=(0, 8))

        # Open the admin status dialog for this issue.
        ctk.CTkButton(
            action_frame,
            text="Update status",
            width=110,
            height=30,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda issue_id=issue.suggestion_id: self.change_status(
                issue_id
            )
        ).pack(anchor="e")

    # Return issues matching the selected admin filters in priority order.
    def get_filtered_suggestions(self, query, category, status):
        # Prepare query text for case-insensitive searching.
        query = query.strip().lower()
        filtered = []

        # Review issues in priority ranking order.
        for issue in self.engine.get_ranked_suggestions():
            # Skip issues outside the selected category.
            if category != "All" and issue.category != category:
                continue

            # Skip issues outside the selected workflow status.
            if status != "All" and issue.status.lower() != status.lower():
                continue

            # Combine relevant values into one searchable string.
            searchable_text = (
                f"{issue.suggestion_id} "
                f"{issue.text} "
                f"{issue.location} "
                f"{issue.category} "
                f"{issue.status} "
                f"{issue.calc_priority_level()}"
            ).lower()

            # Skip issues that do not match the search query.
            if query and query not in searchable_text:
                continue

            # Keep matching issues.
            filtered.append(issue)

        # Return the filtered issue list.
        return filtered


# Run the desktop app only when this file is executed directly.
if __name__ == "__main__":
    app = GUI()
    app.mainloop()
