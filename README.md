# Computer Workshop Application

## Overview

The Computer Workshop application is designed to manage and display custom-built PCs and their components. The application allows users to browse, search, filter, and sort through a collection of PCs and components. Additionally, it provides functionality for master users to create, edit, and delete PCs and components. The application also includes a configurator for custom PC builds and a homepage with statistical summaries.

## Models

### User

- `email`: Unique email address for the user.
- `is_master`: Boolean indicating if the user is a master.
- `is_client`: Boolean indicating if the user is a client.

### Component

- `name`: Name of the component.
- `specifications`: Detailed specifications of the component.
- `price`: Price of the component.
- `type`: Type of component (e.g., CPU, GPU, RAM, etc.).

### Master

- `user`: One-to-one relationship with the `User` model.
- `number_of_constructed_computers`: Integer field tracking the number of PCs constructed by the master.

### Client

- `user`: One-to-one relationship with the `User` model.

### Computer

- `name`: Name of the computer.
- `description`: Description of the computer.
- `components`: Many-to-many relationship with the `Component` model.
- `master`: Foreign key relationship with the `Master` model.
- `pc_type`: Type of PC (e.g., Gaming PC, Workstation, etc.).

### Cart

- `client`: One-to-one relationship with the `Client` model.
- `items`: Many-to-many relationship with the `Computer` model.

## Views

### Home View

Displays the homepage with statistical summaries for the number of ready-built PCs, components, and masters.

### Available Computers View

Lists all available computers with options for sorting, filtering by type, and searching by name. Includes pagination.

### Computer Detail View

Displays detailed information about a specific computer.

### Components List View

Lists all components with options for sorting, filtering by type, and searching by name. Includes pagination.

### Configurator View

Allows users to configure a custom PC by selecting components and assigning a master.

### Add to Cart View

Adds a computer to the client's cart.

### Master Dashboard View

Allows master users to add, edit, and delete components.

### Manage Users View

Allows master users to view and manage all users, including editing user information.

## Templates

### base.html

The base template that includes the navigation bar and general structure of the website.

### home.html

The homepage template displaying the statistical summaries.

### available_computers.html

Template for displaying available computers with sorting, filtering, and pagination options.

### computer_detail.html

Template for displaying detailed information about a specific computer.

### components_list.html

Template for displaying components with sorting, filtering, and pagination options.

### configurator.html

Template for the configurator form where users can configure a custom PC.

### add_component.html

Template for the master dashboard where masters can add components.

### manage_users.html

Template for managing users, allowing masters to view and edit user information.

