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
5. Don't ever ever reuse a branch after a PR has been pushed and merged. 


### Differentiation between types of branches:
main: Your branch. You work here.
origin/main: Git’s memory of GitHub’s main.
origin/HEAD: Pointer: “GitHub’s main branch is called main.”

# Correct workflows

## Editing files and merging to the repo

### 1) Start from up-to-date main
Firstly, before creating a new branch, make sure your main is synched to the git hub repo. 

git switch main
git pull -- rebase origin main 

### 2) Create feature branch and switch to it
git switch -c branch-abc

### 3) Work, stage, commit 
This is where you edit files.
You are encouraged to make many commits.

git add .
git commit -m "Implement XYZ"


### 4) Push branch to GitHub (first time)
This is where the work is pushed to git hub.

git push -u origin branch-abc

### 5) On GitHub website
open PR (or Draft PR) branch-abc → main, review, merge

## Cleaning up after a PR merge

### 6) After merge, update local main
git switch main
git pull -- rebase origin main

### 7) Delete remote branch (on GitHub web or use the cli)
git push origin --delete branch-abc
Another useful way that I ended up using
git branch -r (to see them)
git fetch origin --prune (to delete them)

### 8) Delete local branch
git branch -d branch-abc

### If I work on a branch and want to stay up to date with the remote repo (aka rebase):
*First, I can update main (best practice, but not mandatory)*

git switch main

git fetch origin          get the latest info from GitHub

git pull                  or: git pull --rebase if you configured that



*Then, I need to update my feature branch (experienced devs do this without updating main)*

git switch feature-xyz

git rebase main



*If there are conflicts, after fixing them do:*

git add file1 file2 ...

git rebase --continue

Until no more conflicts

*If you want to skip updating main, and just update the feature branch*
From the branch:

git fetch origin

git switch feature-xyz

git rebase origin/main



### Misc

### 9) To safely rebase, run
git pull --rebase

### 10) You could also configure git in advance:
git config --global pull.rebase true

### 11) To really see all the branches, even remote branches that are stored locally
git branch -r

### 12) To kill them
git fetch origin --prune







