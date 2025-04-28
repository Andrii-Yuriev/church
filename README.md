# Religious Atlas (Django Project)

## Description

A Django web application designed to serve as a comprehensive atlas for
information related to various religions, churches, pastors, and disciples. It
features a clean and responsive user interface based on the **Material Kit 2**
design system, providing an organized way to view, manage, and explore data
within these domains.

## Core Features

* **Data Management:** Manages interconnected data for four primary models:
    * **Religion:** Information about different religions.
    * **Church:** Details about specific churches, linked to a Religion.
    * **Pastor:** User model (inheriting from `AbstractUser`) representing
      pastors, potentially linked to a Religion and Churches.
    * **Disciple:** Information about disciples, potentially linked to a Church
      and a mentor Pastor.
* **CRUD Operations:** Full Create, Read, Update, Delete functionality is
  implemented for manageable models (Religion, Church, Disciple, Pastor profile
  editing), allowing for easy data administration.
* **Search Functionality:** Users can search across list views (Religions,
  Churches, Pastors, Disciples) to quickly find relevant information.
* **Pagination:** List views utilize pagination to efficiently handle
  potentially large amounts of data.
* **User Authentication:** Includes custom-styled pages for:
    * Login
    * Logout
    * User Registration
* **Responsive UI:** Integrated **Material Kit 2** for a modern, responsive
  design that adapts to various screen sizes.
* **Views:** Dedicated views for:
    * Homepage providing an overview and entry points.
    * List views for all core models.
    * Detail views for Religion, Church, and Pastor models.
* **Dynamic Data:** Utilizes context processors or direct context injection in
  views to display dynamic counts (e.g., number of religions, churches) in the
  navigation bar.

## Technology Stack

* **Backend:** Python, Django
* **Frontend:** HTML5, CSS3, JavaScript
* **UI Kit:** Material Kit 2 (based on Bootstrap 5)
* **Database:** SQLite

## Installation

To set up and run the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <URL_your_repo>
    cd <project_folder_name>
    ```

2.  **Create a virtual environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

4.  **Install dependencies:**
    Install all required packages using pip and the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (optional, for accessing Django admin):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

    The application should now be running at `http://127.0.0.1:8000/`.