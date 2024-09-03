# Music Streaming Web Application (Upgraded Version)

This **Music Streaming Web Application** represents an upgraded version of our previous project, offering enhanced capabilities and a refined user experience for music enthusiasts and creators alike. Building on the foundation laid by the original application, this version introduces a more dynamic front-end with Vue3 and further improves backend functionalities with Flask and additional technologies. Users can explore, upload, and manage music content with greater ease and efficiency.

## Key Improvements and Technologies Used

- **Python**: Continues to serve as the host programming language, facilitating the development of robust backend controllers.
- **Vue.js**: A new addition to the technology stack, Vue3 is now used to develop a more dynamic and interactive front end.
- **HTML & CSS**: Utilized to develop Vue components and style web pages.
- **Bootstrap**: Enhances the front-end's responsiveness and visual appeal, making it more user-friendly.
- **SQLite**: Serves as the primary database, providing efficient data storage and retrieval.
- **Flask**: Remains the core web framework, managing server-side operations.
  - **Flask-Restful**: Used to create a comprehensive RESTful API for managing the platform's functionalities.
  - **Flask-SQLAlchemy**: Handles database interactions seamlessly within the Flask environment.
  - **Flask-Celery**: Introduced for managing asynchronous background jobs, enhancing backend performance.
  - **Flask-Caching**: Utilized for caching API outputs to improve response times and overall application performance.
  - **Flask-JWT-Extended**: Implements secure authentication and access control through JWT tokens.
- **Redis**: Employed as an in-memory database for caching and as a message broker for Celery, optimizing API performance and task management.
- **Git**: Continues to provide version control, ensuring smooth collaboration and development.

## Enhanced API Design

The API, designed using the Flask-Restful library, offers more robust endpoints for managing authentication, songs, albums, and playlists. It supports full CRUD (Create, Read, Update, Delete) operations, enabling comprehensive management of music content within the platform.

## Upgraded Architecture and Features

This upgraded version adopts a client-server architecture, utilizing Vue.js for front-end operations and Python-Flask for backend processes. Vue.js, with its MVVM architecture, enhances the user interface and experience, while Python-Flask manages server-side logic, including handling HTTP requests, asynchronous tasks, and database operations.

### New and Improved Features

- **Admin Dashboard**: An enhanced dashboard for admins to monitor app statistics and manage users, creators, and albums efficiently.
- **User Authentication**: Improved secure login and registration processes with advanced role-based access control.
- **General User Functionalities**: Users can view songs and albums, read lyrics, rate songs, and create playlists.
- **Creator Functionalities**: Creators have expanded capabilities to add, edit, remove songs and albums, and manage album listings.
- **Search Functionality**: Enhanced search options allow users to find songs and albums by artist and genre more effectively.
- **Backend Jobs**: New scheduling and execution of backend tasks, including exports, reporting, and alerts.
- **Daily Reminder Jobs**: Automated reminders encourage users to engage with the app daily.
- **Monthly Activity Reports**: Automated generation and distribution of detailed progress reports for creators, enhancing insights into content performance.

This version brings a significant upgrade over the previous iteration, offering more functionality, better performance, and an improved user experience.

