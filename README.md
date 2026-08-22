# Cami ![88x31 GIF](images/cami8831.gif)  

> *A simple, silly, and lightweight http only authentication service made by someone with no experience.*

Cami is an authentication service that is being slowly expanded for a few reasons:  
1: I enjoy making chat servers, but have no way to enforce bans, usernames, or any number of things.  
2: I'm bored out of my mind.  
3: I love working on it! It's entirely HTTP based right now, with some websocket work being made for a live chatting service, and online status.   

For web users, just go to the server address /client and register.  
For stardance users, hit try project and register an account.  
For developers read `/docs` for how to interact with the project.  

<img width="504" height="296" alt="image" src="https://github.com/user-attachments/assets/aa012b60-ed97-437a-b46a-609afdb0b574" />

Features:\
TinyDB Databases for long term file storage.\
SHA256 hashing to secure passwords.\
Designed to be easy to use in other projects, even if not running the server locally.\
Register an account.\
Login with the account.\
Tokens are implemented for things that are temporary, and change on login.\
Set a custom bio.\
Get information about a user from username.\
Get information about a user from id.\
Currency.\
A light chatting service similar to a stripped down twitter feed.\
PFPs.\
Image library similar to like Tenor but for pngs/jpgs.\

W.I.P.  
Live chatting over websocket connections!  
Music library where people can upload mp3s and get them back to play them.  

To run locally:  
Simply clone the repo, have Python3, and run: `pip install -r requirements.txt`, `python3 init.py`

Read `/docs` for more information and how to use.
