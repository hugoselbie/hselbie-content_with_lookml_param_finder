import looker_sdk
import configparser as ConfigParser
import datetime


def find_delinquent_users(delinquent_days: int):
    """Find deliquent users passing in an arbitrary days to disable
    number

    Args:
        days_to_disable (int): number in days that you consider users
        to be deliquent

    Returns:
        [list]: list of user ids that can be disabled or deleted that haven't
        logged in for x days
    """
    response = sdk.all_users()
    delinquent_users = []
    for user in range(0, len(response)):
        try:
            login_date = response[user].credentials_saml.logged_in_at
            login_date = datetime.datetime.strptime(login_date[0:10], "%Y-%m-%d")
            days_since_login = abs(datetime.datetime.now() - login_date).days
            if days_since_login < delinquent_days:
                delinquent_users.append(response[user].id)

        except AttributeError:
            print(f'user {response[user].id} did not login through saml')
    return delinquent_users


def disable_deliquent_users(user_list: list):
    """Expects a list of user id's and iterates
    through that list

    Args:
        user_list (list): [a list of looker user ids]

    Returns:
        [list]: [ids of disabled users]
    """
    user_disable_list = []
    for user_id in user_list:
        user_info_body = sdk.user(user_id)
        if user_info_body.verified_looker_employee is False:
            email = user_info_body.credentials_saml.email.split('@')[1]
            if email != 'looker.com':
                info = (f'{user_info_body.credentials_saml.email} would be disabled'
                        'if you uncommented the next line')
                print(info)
                # Comment out the next line to disable users!
                # user_info_body.is_disabled = True
                user_disable_list.append(user_info_body.id)

    return user_disable_list


if __name__ == "__main__":
    ini_file = 'looker.ini'
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(ini_file)

    github_token = config.get('Github', 'github_token')
    sdk = looker_sdk.init31(config_file=ini_file)

    # example usage
    deliquent_users = find_delinquent_users(30)
    print(disable_deliquent_users(deliquent_users))
