# Deployment Instructions

Since you are working in a downloaded folder (`mathurishan.github.io-main`) and not the original Git repository, we need to initialize Git and push your changes to GitHub.

**WARNING**: The following steps will **overwrite** the content on your GitHub repository with the new modernized version.

## Option 1: Using the Command Line (Recommended)

1.  Open your terminal (PowerShell or Command Prompt) in this folder:
    `d:\mathurishan.github.io-main`

2.  Run the following commands one by one:

    ```powershell
    # 1. Initialize a new git repository
    git init

    # 2. Add all new files
    git add .

    # 3. Commit the changes
    git commit -m "Modernize portfolio: Remove jQuery, update design, add SQL page"

    # 4. Rename branch to main
    git branch -M main

    # 5. Add your GitHub repository as remote
    # Make sure this URL is correct!
    git remote add origin https://github.com/mathurishan/mathurishan.github.io.git

    # 6. Push the changes (Force push to replace old files)
    git push -u origin main --force
    ```

## Option 2: Manual Upload (If you prefer GUI)

1.  Go to your GitHub repository: [https://github.com/mathurishan/mathurishan.github.io](https://github.com/mathurishan/mathurishan.github.io)
2.  Click **Add file** > **Upload files**.
3.  Drag and drop **ALL** files and folders from `d:\mathurishan.github.io-main` into the browser window.
4.  Commit the changes.

## Verification
After pushing, wait a few minutes for GitHub Pages to rebuild. Then visit your site at:
[https://mathurishan.github.io](https://mathurishan.github.io)
