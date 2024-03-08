
# Music Streaming and Lyrics Reading Application
This project is a multi-user web application built with Flask for the backend API and Vue.js for the frontend UI. It allows users to stream music, read lyrics, rate songs, create playlists, and manage albums. The application includes role-based access control (RBAC) with separate functionalities for general users, creators, and admins.




## Features

- **Admin Dashboard**: Monitor app statistics and manage users, creators, and albums.
- **User Authentication**: Secure login and registration with role-based access control.
- **General User Functionalities**: View songs/albums, read lyrics, rate songs, create playlists.
- **Creator Functionalities**: Add/edit/remove songs/albums, manage album listings.
- **Search Functionality**: Search albums by artist, genre, filter songs by rating.
- **Backend Jobs**: Schedule and execute export, reporting, and alert tasks.
- **Daily Reminder Jobs**: Remind users to visit the app daily.
- **Monthly Activity Report**: Generate and email progress reports for creators.



## Technologies Used

- **Backend**: Flask, SQLite, Redis, Celery
- **Frontend**: Vue.js, Vuex, Vue Router
- **Authentication**: Flask-Security
- **Database**: SQLAlchemy
- **Caching**: Redis
- **Batch Jobs**: Celery
- **Deployment**: Heroku (optional), WSL (for Windows OS)
## Installation

Clone the repository:

```bash
https://github.com/Aryan8445/Music-Streaming-Application.git
```
Install backend dependencies:
```bash
pip install -r requirements.txt

```