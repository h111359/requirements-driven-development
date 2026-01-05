# Questionnaire for P-013: Requirements add script

**ℹ️ Context**

The request is to provide a quick and easy way to start the Web UI on both Windows and Linux platforms. The preference is to double-click on a file or use another very easy method, avoiding typing commands in the terminal.

---

## Question 1: Platform-Specific Launch Method

**Q: What type of launcher solution would you prefer for starting the Web UI?**

Please choose one:
- [x] **A)** Platform-specific launchers - Separate files for Windows (.bat) and Linux (.sh)
  - **Pros:** Native feel for each platform, can leverage OS-specific features, familiar to users
  - **Cons:** Need to maintain two files, users must know which file to use
  
- [ ] **B)** Python launcher script with OS-specific wrapper files - Single Python script with .bat and .sh wrappers
  - **Pros:** Core logic in one place, easier maintenance, consistent behavior across platforms
  - **Cons:** Slight overhead, still requires wrapper files
  
- [ ] **C)** Single cross-platform launcher - Python script that can be executed directly
  - **Pros:** One file to maintain, simplest approach
  - **Cons:** May require terminal on some systems, less "double-click" friendly on Windows
  
- [ ] **D)** Desktop shortcuts/launchers - Create OS-specific desktop entry files
  - **Pros:** Most user-friendly (icons, proper OS integration)
  - **Cons:** More complex setup, different mechanisms per OS
  
- [ ] **E)** Other (please specify): 

**Recommendation:** Option B - provides good balance between ease of use and maintainability

---

## Question 2: Browser Launch Behavior

**Q: Should the launcher automatically open the Web UI in the default browser?**

- [x] **Yes** - Automatically open browser after server starts
  - **→** Most convenient, fully automated experience
  
- [ ] **No** - Display URL in console, let user open manually
  - **→** Gives user control over which browser to use
  
- [ ] **Ask on launch** - Prompt user each time whether to open browser
  - **→** Flexible but requires user interaction

**Recommendation:** Yes - aligns with the goal of minimal user effort

---

## Question 3: Server Port Configuration

**Q: How should the Web UI server port be determined?**

- [ ] **A)** Fixed default port (e.g., 8080)
  - **Pros:** Simple, predictable
  - **Cons:** May conflict with other services
  
- [x] **B)** Auto-detect available port
  - **Pros:** Prevents conflicts, always works
  - **Cons:** URL changes between launches
  
- [ ] **C)** Fixed default with auto-fallback if occupied
  - **Pros:** Predictable when possible, reliable when port is occupied
  - **Cons:** Slightly more complex logic
  
- [ ] **D)** Other (please specify): ___________

**Recommendation:** Option C - balances predictability with reliability

---

## Question 4: Error Handling and Feedback

**Q: How should the launcher handle errors (e.g., Python not found, port conflicts)?**

- [x] **A)** Display error in terminal/console window that stays open
  - **Pros:** User can read the error message
  - **Cons:** Still uses terminal window
  
- [ ] **B)** Show error in GUI dialog box
  - **Pros:** More user-friendly, no terminal needed
  - **Cons:** Requires additional dependencies or platform-specific code
  
- [ ] **C)** Log to file and display simple message
  - **Pros:** Errors are preserved, simple implementation
  - **Cons:** User must find and read log file
  
- [ ] **D)** Other (please specify): ___________

**Recommendation:** Option A for simplicity, though Option B is more aligned with avoiding terminal

---

## Question 5: Launcher File Location

**Q: Where should the launcher file(s) be placed?**

- [ ] **A)** Project root directory
  - **Pros:** Immediately visible, easy to find
  - **Cons:** Clutters root directory
  
- [x] **B)** `.rdd/` directory
  - **Pros:** Organized with framework files
  - **Cons:** Less visible, requires navigation
  
- [ ] **C)** `.rdd/launchers/` or similar subdirectory
  - **Pros:** Organized, dedicated location
  - **Cons:** More navigation required
  
- [ ] **D)** Both root (symlink/shortcut) and organized location
  - **Pros:** Visibility and organization
  - **Cons:** More complex setup
  
- [ ] **E)** Other (please specify):

**Recommendation:** Option A - maximizes ease of access for double-click launching

---

## Question 6: Server Shutdown Method

**Q: How should users stop the Web UI server when done?**

- [ ] **A)** Close terminal window (Ctrl+C)
  - **Pros:** Standard approach
  - **Cons:** Requires terminal interaction
  
- [ ] **B)** Provide "Shutdown" button in Web UI
  - **Pros:** No terminal needed, user-friendly
  - **Cons:** Requires implementation in UI
  
- [x] **C)** Both options available
  - **Pros:** Maximum flexibility
  - **Cons:** More implementation work
  
- [ ] **D)** Other (please specify): ___________

**Recommendation:** Option C - aligns with minimizing terminal usage while providing fallback

---

## Question 7: Launcher Naming Convention

**Q: What should the launcher file(s) be named?**

- [ ] **A)** Simple descriptive names: `start-webui.bat` / `start-webui.sh`
  - **Pros:** Clear purpose, easy to understand
  - **Cons:** Generic
  
- [ ] **B)** Product-branded names: `rdd-webui.bat` / `rdd-webui.sh`
  - **Pros:** Clearly associated with RDD
  - **Cons:** Slightly longer
  
- [ ] **C)** Very short names: `start.bat` / `start.sh`
  - **Pros:** Quick to type if needed
  - **Cons:** Not specific, may conflict
  
- [x] **D)** Other (please specify): rdd.bat and rdd.sh

**Recommendation:** Option A - clear and self-documenting
