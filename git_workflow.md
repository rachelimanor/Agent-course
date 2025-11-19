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