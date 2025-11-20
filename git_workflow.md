            ┌──────────────────────────────┐
            │        MAIN (protected)      │
            │   ❌ Cannot push directly     │
            └──────────────┬───────────────┘
                           │
                           │ git switch -c feature-xyz
                           ▼
              ┌──────────────────────────┐
              │   feature-xyz (local)    │
              │   ✔ You write code here  │
              └──────────────┬───────────┘
                             │
                             │ git add .
                             │ git commit -m "message"          This is the local commit to the feature branch
                             │
                             ▼
              ┌──────────────────────────┐
              │ feature-xyz (pushed)     │
              │   on GitHub remote       │
              └──────────────┬───────────┘
                             │
                             │ git push -u origin feature-xyz   This is the push to the origin (remote repo). Git prompts the user to create a PR.
                             ▼
               ┌─────────────────────────┐
               │   Pull Request (PR)     │
               │  feature-xyz → main     │
               │   ✔ Review & merge      │
               └──────────────┬──────────┘
                              │
                              │ GitHub merges PR
                              ▼
            ┌──────────────────────────────┐
            │        MAIN (updated)        │
            │   ✔ Your changes are live    │
            └──────────────────────────────┘


A few other important things:
1. Afterwords, delete the branch by applying: git branch -d feature-xyz
2. To see all commits, run: git log --oneline
3. To see all edited files: git status 
4. To pull from repo: git pull


## Correct workflow

# 1) Start from up-to-date main
git switch main
git pull origin main

# 2) Create feature branch and switch to it
git switch -c branch-abc

# 3) Work, stage, commit
# ...edit files...
git add .
git commit -m "Implement XYZ"

# 4) Push branch to GitHub (first time)
git push -u origin branch-abc

# 5) On GitHub: open PR (or Draft PR) branch-abc → main, review, merge

# 6) After merge, update local main
git switch main
git pull origin main

# 7) Delete remote branch (on GitHub or:)
# git push origin --delete branch-abc

# 8) Delete local branch
git branch -d branch-abc

# 9) To safely rebase, run
git pull --rebase

# 10) You could also configure git in advance:
git config --global pull.rebase true

