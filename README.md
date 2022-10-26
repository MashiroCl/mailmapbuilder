# mailmapbuilder

Automatically build .mailmap for a git repository


## Introduciton
[.mailmap](https://git-scm.com/docs/gitmailmap) is used to map author and committer names and email addresses to canonical real names and email addresses. 
With mailmapbuilder, the .mailmap file can be automatically built.

## How it works
It uses the [GitHub API](https://docs.github.com/en/rest/quickstart) and the [commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)
to build the .mailmap:
- Extract developers names and emails from the commit hisotry
- Use the [GitHub Search Uesr API](https://docs.github.com/en/rest/search#search-users) and developer name as the parameter to search the developer's GitHub personal page
- Select the top searched result as the candidate
- Extract the developer's login and public email from the candidate
- Use the login, public email to search in the commit history to collect the develoepr's aliases and emails in a chained way

## Requirement
python3.7 and later

## Build
1. **Clone this repository and install dependencies**

```
$ git clone https://github.com/MashiroCl/mailmapbuilder
$ cd mailmapbuilder
$ pip install -r requirements.txt
```

2. **Creating a personal access token**

The mailmapbuilder uses the GitHub API, it needs te personal access token to run.

For how to get personal access token, please refer to [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

3. **Set the token as a environment variable**

After you get the token, set it as an environment variable, and named the variable as **MAILMAPBUILDER**

For MacOS:
```
$ echo "export MAILMAPBUILDER=<personal-access-token>" >> ~/.bash_profile
$ source ~/.bash_profile
```

For Linux:
```
export MAILMAPBUILDER=<personal-access-token>
```

## Run Example
```
$ python3 run.py -i <path-for-repository> -o <path-for-repository>
```

## General Options
- `-i`, `--input`: path for repository need to be built .mailmap
- `-o`, `--output`:output path for .mailmap file


