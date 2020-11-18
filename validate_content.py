from looker_sdk import models
import looker_sdk
import configparser as ConfigParser
import hashlib
import logging


logging.basicConfig(level=logging.DEBUG)


def get_space_data():
    """Collect all space information"""
    space_data = sdk.all_spaces(fields="id, parent_id, name")
    return space_data


def parse_broken_content(base_url, broken_content, space_data):
    """Parse and return relevant data from content validator"""
    output = []
    for item in broken_content:
        if item.dashboard:
            content_type = "dashboard"
        else:
            content_type = "look"
        item_content_type = getattr(item, content_type)
        id = item_content_type.id
        name = item_content_type.title
        space_id = item_content_type.space.id
        space_name = item_content_type.space.name
        errors = item.errors
        url = f"{base_url}/{content_type}s/{id}"
        space_url = "{}/spaces/{}".format(base_url, space_id)
        if content_type == "look":
            element = None
        else:
            dashboard_element = item.dashboard_element
            element = dashboard_element.title if dashboard_element else None
        # Lookup additional space information
        space = next(i for i in space_data if str(i.id) == str(space_id))
        parent_space_id = space.parent_id
        # Old version of API  has issue with None type for all_space() call
        if parent_space_id is None or parent_space_id == "None":
            parent_space_url = None
            parent_space_name = None
        else:
            parent_space_url = "{}/spaces/{}".format(base_url, parent_space_id)
            parent_space = next(
                (i for i in space_data if str(i.id) == str(parent_space_id)), None
            )
            # Handling an edge case where space has no name. This can happen
            # when users are improperly generated with the API
            try:
                parent_space_name = parent_space.name
            except AttributeError:
                parent_space_name = None
        # Create a unique hash for each record. This is used to compare
        # results across content validator runs
        unique_id = hashlib.md5(
            "-".join(
                [str(id), str(element), str(name), str(errors), str(space_id)]
            ).encode()
        ).hexdigest()
        data = {
            "content_id": str(id),
            "unique_id": unique_id,
            "content_type": content_type,
            "name": name,
            "url": url,
            "dashboard_element": element,
            "space_name": space_name,
            "space_url": space_url,
            "parent_space_name": parent_space_name,
            "parent_space_url": parent_space_url,
            "errors": str(errors),
        }
        output.append(data)
    return output


def sendContentOnce(**kwargs):
    content_type = kwargs.get('content_type')
    content_id = kwargs.get('content_id')
    user_id = kwargs.get('user_id')
    plan_id = kwargs.get('plan_id')
    user_email = kwargs.get('user_email')
    message = kwargs.get('message')
    logging.debug(f'Assigned variables content_type:{content_type}')

    plan_destination = [
        {
            "id": 10,
            "scheduled_plan_id": plan_id,
            "format": "inline_json",
            "address": f"{user_email}",
            "type": "email",
            "message": f"{message}",
        }
    ]
    if content_type == 'dashboard':
        splan = models.WriteScheduledPlan(
            name='test1',
            dashboard_id=content_id,
            user_id=user_id,
            require_no_results=False,
            require_change=False,
            require_results=True,
            include_links=False,
            scheduled_plan_destination=plan_destination
        )
        sdk.scheduled_plan_run_once(body=splan)
    elif content_type == 'look':
        splan = models.WriteScheduledPlan(
            name='test1',
            look_id=content_id,
            user_id=user_id,
            require_no_results=False,
            require_change=False,
            require_results=True,
            include_links=False,
            scheduled_plan_destination=plan_destination
        )
        # sdk.scheduled_plan_run_once(body=splan)

    return f'notification for {content_id} has been sent to {user_email}'


def sendContentAlert(broken_content: list):
    logging.debug('Initializing sendContentAlert')
    for content in range(0, len(broken_content)):
        logging.debug(broken_content[content]['content_type'])
        logging.debug(broken_content[content]['content_id'])
        if broken_content[content]['content_type'] == 'dashboard':
            dashboard_metadata = sdk.dashboard(str(broken_content[content]['content_id']))
            user_id = dashboard_metadata.user_id
            user_email = sdk.user(user_id=user_id).email
            content_url = broken_content[content]['content_id']
            logging.debug(f'variables set user_id:{user_id}, user_email:{user_email}, content_url {content_url}')

            sendContentOnce(
                user_id=user_id,
                user_email=user_email,
                plan_id=content,
                content_id=19,
                content_type='dashboards',
                message=f'please fix or delete your content {content_url}'
            )

        elif broken_content[content]['content_type'] == 'look':
            look_metadata = sdk.look(broken_content[content]['content_id'])
            user_id = look_metadata.user_id
            content_url = look_metadata.short_url
            user_email = sdk.user(user_id=user_id).email

            sendContentOnce(
                user_id=user_id,
                user_email=user_email,
                plan_id=content,
                content_id=5,
                content_type='look',
                message=f'please fix or delete your content {content_url}'
            )

    return 'complete'


if __name__ == "__main__":
    ini_file = '/usr/local/google/home/hugoselbie/code_sample/py/projects/ini/looker.ini'
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(ini_file)

    github_token = config.get('Github', 'github_token')
    sdk = looker_sdk.init31(config_file=ini_file)

    x = sdk.content_validation().content_with_errors
    space = get_space_data()

    broken_content = parse_broken_content(
        broken_content=x,
        space_data=space,
        base_url='https://34.94.160.95'
    )
    # print(broken_content[0])

    print(sendContentAlert(broken_content=broken_content))

    # print(test(
    #     user_id=5,
    #     user_email='hseli',
    #     plan_id=6,
    #     content_id=45,
    #     content_type='test'
    # ))
