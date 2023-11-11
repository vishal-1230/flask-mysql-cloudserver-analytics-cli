# Flask MySQL Cloud Analytics CLI

## Introduction

This is a command-line interface (CLI) written in Python to connect to a cloud server over SSH and perform various tasks based on a provided keyword. The tool uses Flask, MySQL, and Paramiko to achieve this functionality.

## Features

- Connects to a cloud server over SSH using provided credentials.
- Retrieves Flask server logs.
- Fetches analytics data from a MySQL database, including user counts, bot counts, message counts, and more.
- Executes custom MySQL queries on the server.
- Provides an overview of the database, including user details and other relevant information.

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vishal-1230/flask-mysql-cloudserver-analytics-cli.git
   ```

2. **Install the required dependencies:**

   ```bash
   pip install paramiko
   ```

3. **Set the required environment variables:**

   ```bash
   export SERVER_IP=<server_ip>
   export SERVER_USERNAME=<server_username>
   export SERVER_PASSWORD=<server_password>
   export SSH_KEY=<path_to_ssh_key>
   export SERVER_MYSQL_USERNAME=<server_mysql_username>
   export SERVER_MYSQL_PASSWORD=<server_mysql_password>
   export SERVER_MYSQL_DATABASE=<server_mysql_database>
   ```

## Usage

To run the CLI, use the following command:

  ```bash
  python main.py <data_type> [options]
  ```

Replace ```<data_type>``` with the type of data you want to retrieve. Here are some examples:

```bash
positional arguments:
  data_type            Type of data to retrieve : fogs, ucount, udetails, bcount, mcount, chatted_people_count, users

optional arguments:
  -h, --help           show this help message and exit
  --email_id EMAIL_ID  Email ID of user to retrieve details for
  --count COUNT        Count of data to retrieve
  --table TABLE        Table of data to retrieve
  --columns COLUMNS    Columns of data to retrieve seperated by space, to be used with users & udetails
  --unique             Get unique data
  --with-users         Get overview with users details
  --query QUERY        Query to execute
```

For detailed usage instructions, run:
  ```bash
  python main.py --help
  ```

If you're on Linux, you can add Alias in you ```~/.bashrc``` file like ```server = source path_to_this_folder/bin/activate && python main.py``` and then just it this from anywhere in your terminal as ```server execute_query 'select * from cool_table;'```

## License

This project is licensed under the MIT License.
