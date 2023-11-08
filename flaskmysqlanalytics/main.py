import paramiko
import os
import argparse
import pprint

def connect_to_server():
    # Connect to server using abc.pem file in Downloads directory
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ip = os.environ.get('SERVER_IP')
    username = os.environ.get('SERVER_USERNAME')
    plain_password = os.environ.get('SERVER_PASSWORD')
    pem_key_path = os.environ.get('SSH_KEY')
    if ip and username and plain_password:
        ssh.connect(hostname=ip, username=username, password=plain_password)
    elif ip and username and pem_key_path:
        key = paramiko.RSAKey.from_private_key_file(os.path.expanduser(pem_key_path))
        ssh.connect(hostname=ip, username=username, pkey=key)
    else:
        print(
"""Please set SERVER_IP, SERVER_USERNAME, SERVER_PASSWORD or SSH_KEY, SERVER_MYSQL_USERNAME, SERVER_MYSQL_PASSWORD, SERVER_MYSQL_DATABASE environment variables.
Set these using the following commands:
export SERVER_IP=<server_ip>
export SERVER_USERNAME=<server_username>
export SERVER_PASSWORD=<server_password>
export SSH_KEY=<path_to_ssh_key>"""
        )
        return False
    print("Connected to server")
    return ssh

# Getting flask server logs, having logs.log file in provided path
def get_flask_logs():
    # Get Flask logs from server
    ssh = connect_to_server()
    stdin, stdout, stderr = ssh.exec_command('tail -n 100 ~/humanize-backend/logs.log')
    logs = stdout.read().decode()
    ssh.close()
    return logs

# Getting user count from humanize database, users table
def get_user_count():
    # Get count of users table in humanize database
    ssh = connect_to_server()
    username = os.environ.get('SERVER_MYSQL_USERNAME')
    password = os.environ.get('SERVER_MYSQL_PASSWORD')
    database = os.environ.get('SERVER_MYSQL_DATABASE')
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.users;"'.format(username, password, database))
    total_count = stdout.read().decode().strip()
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.users WHERE createdAt > DATE_SUB(NOW(), INTERVAL 1 MONTH);"'.format(username, password, database)) # this returns count of users in the last month
    month_count = stdout.read().decode().strip()
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.users WHERE createdAt > DATE_SUB(NOW(), INTERVAL 1 WEEK);"'.format(username, password, database)) # this returns count of users in the last week
    week_count = stdout.read().decode().strip()
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.users WHERE createdAt > DATE_SUB(NOW(), INTERVAL 1 DAY);"'.format(username, password, database)) # this returns count of users in the last day
    day_count = stdout.read().decode().strip()
    count = {
        "Total Users": total_count.lstrip("COUNT(*)\n"),
        "This Month": month_count.lstrip("COUNT(*)\n"),
        "This Week": week_count.lstrip("COUNT(*)\n"),
        "Today's Signups": day_count.lstrip("COUNT(*)\n")
    }
    ssh.close()
    return count

def get_users(count=10, columns='name email_id bots createdAt'):
    # Get latest users from humanize database
    username = os.environ.get('SERVER_MYSQL_USERNAME')
    password = os.environ.get('SERVER_MYSQL_PASSWORD')
    database = os.environ.get('SERVER_MYSQL_DATABASE')
    ssh = connect_to_server()
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT {} FROM {}.users ORDER BY createdAt DESC LIMIT {};"'.format(username, password, columns.replace(" ", ", "), database, count))
    users = stdout.read().decode().strip()
    ssh.close()
    return users

def get_user_details(email_id, columns='name email_id bots createdAt'):
    # Get details of user with given email_id from humanize database
    ssh = connect_to_server()
    username = os.environ.get('SERVER_MYSQL_USERNAME')
    password = os.environ.get('SERVER_MYSQL_PASSWORD')
    database = os.environ.get('SERVER_MYSQL_DATABASE')
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT {} FROM {}.users WHERE email_id=\'{}\'"'.format(username, password, columns.replace(" ", ", "), database, email_id))
    details = stdout.read().decode().strip()
    ssh.close()
    return details

def get_bot_count():
    # Get count of bots in humanize database
    ssh = connect_to_server()
    username = os.environ.get('SERVER_MYSQL_USERNAME')
    password = os.environ.get('SERVER_MYSQL_PASSWORD')
    database = os.environ.get('SERVER_MYSQL_DATABASE')
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.bots;"'.format(username, password, database))
    total_count = stdout.read().decode().strip()
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.bots WHERE createdAt > DATE_SUB(NOW(), INTERVAL 1 MONTH);"'.format(username, password, database)) # this returns count of bots in the last month
    month_count = stdout.read().decode().strip()
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.bots WHERE createdAt > DATE_SUB(NOW(), INTERVAL 1 WEEK);"'.format(username, password, database)) # this returns count of bots in the last week
    week_count = stdout.read().decode().strip()
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.bots WHERE createdAt > DATE_SUB(NOW(), INTERVAL 1 DAY);"'.format(username, password, database)) # this returns count of bots in the last day
    day_count = stdout.read().decode().strip()
    count = {
        "Total Bots": total_count.lstrip("COUNT(*)\n"),
        "This Month": month_count.lstrip("COUNT(*)\n"),
        "This Week": week_count.lstrip("COUNT(*)\n"),
        "Today's Bots": day_count.lstrip("COUNT(*)\n")
    }
    ssh.close()
    return count

def get_message_count(unique=False):
    # Get count of messages in humanize database
    ssh = connect_to_server()
    username = os.environ.get('SERVER_MYSQL_USERNAME')
    password = os.environ.get('SERVER_MYSQL_PASSWORD')
    database = os.environ.get('SERVER_MYSQL_DATABASE')
    if not unique:
        stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.messages;"'.format(username, password, database))
        total_count = stdout.read().decode().strip()
        stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.messages WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 MONTH);"'.format(username, password, database)) # this returns count of messages in the last month
        month_count = stdout.read().decode().strip()
        stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.messages WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 WEEK);"'.format(username, password, database)) # this returns count of messages in the last week
        week_count = stdout.read().decode().strip()
        stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(*) FROM {}.messages WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY);"'.format(username, password, database)) # this returns count of messages in the last day
        day_count = stdout.read().decode().strip()
    else:
        stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(DISTINCT username) FROM {}.messages;"'.format(username, password, database))
        total_count = stdout.read().decode().strip()
        stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(DISTINCT username) FROM {}.messages WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 MONTH);"'.format(username, password, database))
        month_count = stdout.read().decode().strip()
        stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(DISTINCT username) FROM {}.messages WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 WEEK);"'.format(username, password, database))
        week_count = stdout.read().decode().strip()
        stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(DISTINCT username) FROM {}.messages WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY);"'.format(username, password, database))
        day_count = stdout.read().decode().strip()
    count = {
        "Total": total_count.lstrip("COUNT(*)\n"),
        "This Month": month_count.lstrip("COUNT(*)\n"),
        "This Week": week_count.lstrip("COUNT(*)\n"),
        "Today's Chats": day_count.lstrip("COUNT(*)\n")
    }
    ssh.close()
    return count

def get_chatted_people_count():
    # Get count of people who chatted in humanize database
    ssh = connect_to_server()
    username = os.environ.get('SERVER_MYSQL_USERNAME')
    password = os.environ.get('SERVER_MYSQL_PASSWORD')
    database = os.environ.get('SERVER_MYSQL_DATABASE')
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT COUNT(DISTINCT username) FROM {}.messages;"'.format(username, password, database))
    count = stdout.read().decode().strip()
    ssh.close()
    return count

def overview(with_users=False):
    # Get overview of humanize database
    ucount = get_user_count()
    bcount = get_bot_count()
    mcount = get_message_count()
    if with_users:
        users = get_users()
    else:
        users = None

    if users:
        overview = {
            "Users Count": ucount,
            "Bots Count": bcount,
            "Messages Count": mcount,
            "Users": users
        }
    else:
        overview = {
            "Users Count": ucount,
            "Bots Count": bcount,
            "Messages Count": mcount
        }
    return overview

# getting any tables, columns from humanize database
def get_data(table, columns, count=10):
    # Get data from humanize database
    ssh = connect_to_server()
    username = os.environ.get('SERVER_MYSQL_USERNAME')
    password = os.environ.get('SERVER_MYSQL_PASSWORD')
    database = os.environ.get('SERVER_MYSQL_DATABASE')
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "SELECT {} FROM {}.{} ORDER BY createdAt DESC LIMIT {};"'.format(username, password, columns.replace(" ", ", "), database, table, count))
    data = stdout.read().decode().strip()
    ssh.close()
    return data

# execute any mysql query
def execute_query(query):
    # Execute any mysql query
    ssh = connect_to_server()
    username = os.environ.get('SERVER_MYSQL_USERNAME')
    password = os.environ.get('SERVER_MYSQL_PASSWORD')
    database = os.environ.get('SERVER_MYSQL_DATABASE')
    stdin, stdout, stderr = ssh.exec_command('mysql -u {} -p{} -e "{}"'.format(username, password, query))
    data = stdout.read().decode().strip()
    ssh.close()
    return data

def start():
    parser = argparse.ArgumentParser(description='Get data from server')
    parser.add_argument('data_type', type=str, help='Type of data to retrieve : fogs, ucount, udetails, bcount, mcount, chatted_people_count, users')
    parser.add_argument('--email_id', type=str, help='Email ID of user to retrieve details for')
    parser.add_argument("--count", type=int, help="Count of data to retrieve")
    parser.add_argument("--table", type=str, help="Table of data to retrieve")
    parser.add_argument("--columns", type=str, help="Columns of data to retrieve seperated by space, to be used with users & udetails")
    parser.add_argument("--unique", action="store_true", help="Get unique data")
    parser.add_argument("--with-users", action="store_true", help="Get overview with users details")
    parser.add_argument("--query", type=str, help="Query to execute")
    args = parser.parse_args()

    sql_username = os.environ.get('SERVER_MYSQL_USERNAME')
    sql_password = os.environ.get('SERVER_MYSQL_PASSWORD')
    sql_database = os.environ.get('SERVER_MYSQL_DATABASE')

    if sql_username and sql_password and sql_database:
        sql_creds_provided = True
    else:
        sql_creds_provided = False
        print(
"""
Please set SERVER_MYSQL_USERNAME, SERVER_MYSQL_PASSWORD, SERVER_MYSQL_DATABASE environment variables.
Set these using the following commands:

export SERVER_MYSQL_USERNAME=<server_mysql_username>
export SERVER_MYSQL_PASSWORD=<server_mysql_password>
export SERVER_MYSQL_DATABASE=<server_mysql_database>
"""
        )

    if args.data_type == 'fogs':
        print(get_flask_logs())
    elif args.data_type == 'ucount' and sql_creds_provided:
        user = (get_user_count())
        for key, value in user.items():
            print(key, ':', value)
    elif args.data_type == 'udetails' and sql_creds_provided:
        if args.email_id:
            if args.columns:
                pprint.pprint(get_user_details(args.email_id, args.columns))
            else:
                pprint.pprint(get_user_details(args.email_id))
        else:
            print('Email ID not provided')
    elif args.data_type == 'bcount' and sql_creds_provided:
        bots = get_bot_count()
        for key, value in bots.items():
            print(key, ':', value)
    elif args.data_type == 'mcount' and sql_creds_provided:
        if args.unique:
            for key, value in get_message_count(unique=True).items():
                print(key, ':', value)
        else:
            for key, value in get_message_count().items():
                print(key, ':', value)
    elif args.data_type == 'chatted_people_count' and sql_creds_provided:
        print(get_chatted_people_count())
    elif args.data_type == 'users' and sql_creds_provided:
        if args.count:
            if args.columns:
                # pprint.pprint(get_users(args.count, args.columns))
                # format the tuple returned in terminal
                users = get_users(args.count, args.columns)
                users = users.split('\n')
                users = [user.split('\t') for user in users]
                for user in users:
                    print(user)
            else:
                # pprint.pprint(get_users(args.count))
                # format the tuple returned in terminal
                users = get_users(args.count)
                users = users.split('\n')
                users = [user.split('\t') for user in users]
                for user in users:
                    print(user)
        else:
            # pprint.pprint(get_users())
            # format the tuple returned in terminal
            users = get_users()
            users = users.split('\n')
            users = [user.split('\t') for user in users]
            for user in users:
                print(user)
    elif args.data_type == 'overview' and sql_creds_provided:
        if args.with_users:
            for key, value in overview(with_users=True).items():
                print("\n\033[1m\033[34m"+key+"\033[0m")
                if key == "Users":
                    value = value.split('\n')
                    value = [user.split('\t') for user in value]
                    for user in value:
                        print(user)
                else:
                    for k, v in value.items():
                        print(k, ':', v)
        else:
            for key, value in overview().items():
                print("\n\033[1m\033[34m"+key+"\033[0m")
                if key == "Users":
                    value = value.split('\n')
                    value = [user.split('\t') for user in value]
                    for user in value:
                        print(user)
                else:
                    for k, v in value.items():
                        print(k, ':', v)
    elif args.data_type == 'execute_query' and sql_creds_provided:
        if args.query:
            print(execute_query(args.query))
        else:
            print('Query not provided')
    elif args.data_type == 'get_data' and sql_creds_provided:
        if args.table and args.columns:
            if args.count:
                data = get_data(args.table, args.columns, args.count)
                data = data.split('\n')
                data = [row.split('\t') for row in data]
                for row in data:
                    print(row)
            else:
                data = get_data(args.table, args.columns)
                data = data.split('\n')
                data = [row.split('\t') for row in data]
                for row in data:
                    print(row)
        else:
            print('Table or columns not provided')
    else:
        print('Invalid data type provided')

if __name__ == '__main__':
    start()

# latest users (optional count of users, default 10, optional columns, default name, email_id, createdAt)
# latest bots with username (")
# latest messages (optional count of messages, default 10, optional columns, default username, botid, timstamp)
