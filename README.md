# Computer Workshop Application

## Overview

The Computer Workshop application is designed to manage and display custom-built PCs and their components. The application allows users to browse, search, filter, and sort through a collection of PCs and components. Additionally, it provides functionality for master users to create, edit, and delete PCs and components. The application also includes a configurator for custom PC builds and a homepage with statistical summaries.

---

# Site Review Data

To review the site and access different functionalities, use the following credentials:

## Site URL: [Computer Workshop](https://computer-workshop.onrender.com)


### Master User
- **Username**: `master`
- **Password**: `112233QWEasd`

### Client User
- **Username**: `client`
- **Password**: `112233QWEasd`

This information will allow you to explore the site from different user perspectives and access various features.



## How to Install

To set up the Django project on your local machine, follow these steps:

### Prerequisites

- Python 3.8+
- Django 3.2+
- Virtualenv (recommended)


## How to Install

To set up the Django project on your local machine, follow these steps:

### Prerequisites

- Python 3.8+
- Django 3.2+
- Virtualenv (recommended)

### Step-by-Step Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/Gilgumish/computer-workshop
   cd computer-workshop

2. **Set Up Virtual Environment**

   For Unix-based systems:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
   For Windows systems:
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add:

   ```sh
   SECRET_KEY=your_secret_key
   DEBUG=True
   PGDATABASE=your_database_name
   PGUSER=your_database_user
   PGPASSWORD=your_database_password
   PGHOST=your_database_host
   PGPORT=your_database_port
   ```

5. **Apply Migrations**

   ```sh
   python manage.py migrate
   ```

6. **Create a Superuser**

   ```sh
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```sh
   python manage.py runserver
   ```

8. **Access the Application**

   Navigate to `http://127.0.0.1:8000`.
### Optional: Load Initial Data

If your project includes fixtures or initial data, you can load them using:

```sh
python import_data.py
```

### Running Tests

To run the test suite:

```sh
python manage.py test
```


## DB-structure diagram

![Computer Workshop DB-structure diagram](pc_workshop.png)


## Models

### User

- `email`: Unique email address for the user.
- `is_master`: Boolean indicating if the user is a master.
- `is_client`: Boolean indicating if the user is a client.
- `number_of_constructed_computers`: Integer field tracking the number of PCs constructed by the master. This field is only relevant for master users.

### Component

- `name`: Name of the component.
- `specifications`: Detailed specifications of the component.
- `price`: Price of the component.
- `type`: Type of component (e.g., CPU, GPU, RAM, etc.).

### Computer

- `name`: Name of the computer.
- `description`: Description of the computer.
- `components`: Many-to-many relationship with the `Component` model.
- `master`: Foreign key relationship with the `User` model, where the user is a master.
- `pc_type`: Type of PC (e.g., Gaming PC, Workstation, etc.).

### Cart

- `client`: Foreign key relationship with the `User` model, where the user is a client.
- `components`: Many-to-many relationship with the `Component` model.
- `computers`: Many-to-many relationship with the `Computer` model.
- `master`: Foreign key relationship with the `User` model, where the user is a master.

## Application Functionality Overview

The application provides a variety of functionalities for managing a computer workshop, including user management, component and computer management, custom PC configuration, and cart operations. Below is a description of each functionality.

### Home View
- **Function**: Displays the homepage with counts of available computers, components, and masters.

### Available Computers View
- **Function**: Lists all available computers with pagination and sorting options (by name, type, and price). Provides search functionality.

### Computer Detail View
- **Function**: Displays detailed information about a specific computer.

### User Authentication Views
- **Login**: Displays and processes the login form.
- **Register**: Displays and processes the registration form.

### Configurator View
- **Function**: Allows users to configure a custom PC by selecting components and a master. Adds the configured components to the user's cart.

### Add Computer View
- **Function**: Allows masters to add new computers to the system.

### Available Components View
- **Function**: Lists all available components with pagination and sorting options (by name, type, and price). Provides search functionality.

### Manage Users View
- **Function**: Allows superusers and masters to manage users. Provides search and filter functionality and displays a paginated list of users.

### View User Cart View
- **Function**: Allows masters to view the cart of a specific client.

### Component Management Views
- **Edit Component**: Allows masters to edit existing components.
- **Delete Component**: Allows masters to delete components.
- **Add Component**: Allows masters to add new components to the system.

### Computer Management Views
- **Edit Computer**: Allows masters to edit existing computers.
- **Delete Computer**: Allows masters to delete computers.

### Cart Management Views
- **Add Component to Cart**: Allows clients to add components to their cart.
- **Add Computer to Cart**: Allows clients to add computers to their cart.
- **View Cart**: Displays the contents of the client's cart.
- **Remove from Cart**: Allows clients to remove items from their cart.
- **Clear Cart**: Allows clients to clear all items from their cart.
- **Remove Master from Cart**: Allows clients to remove the master from their cart.

### Edit User View
- **Function**: Allows superusers to edit user information.


## Future Development Prospects for the Computer Workshop Application

The Computer Workshop application has a solid foundation with its current features, but there are several areas where we can expand and improve the functionality and user experience. Here are some key prospects for future development:

### 1. Performance Analytics Integration
When clients configure a PC using the configurator, the system can automatically fetch and display performance data based on the selected components. This can be achieved by parsing information from various benchmarking and review websites. Key metrics could include:
- Gaming performance (FPS in popular games)
- Productivity benchmarks (e.g., video rendering times, software compilation times)
- Power consumption and thermal performance

### 2. Enhanced User Interface and User Experience
Improving the design and usability of the site will make it more engaging and easier to navigate. Potential enhancements include:
- Modernizing the UI with a more visually appealing design
- Implementing responsive design to ensure optimal performance on all devices
- Enhancing the configurator interface with real-time feedback and visual representation of the configured PC
- Adding drag-and-drop functionality for component selection

### 3. Automated Compatibility Checks
Integrate a system that automatically checks for compatibility issues between selected components. This would help prevent configurations that won't work together, improving the user experience and reducing the likelihood of user error.

### 4. User Reviews and Ratings

### 5. Inventory Management
Add features for managing inventory levels of components and pre-built PCs. This can include:
- Stock level tracking
- Automated notifications for low stock
- Integration with suppliers for real-time stock updates

### 6. Advanced Search and Filter Options
Enhance the search functionality with more advanced filters and sorting options, including:
- Filtering by performance metrics
- Sorting by popularity or user ratings
