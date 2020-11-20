import looker_sdk
# import pandas as pd
import json
from looker_sdk import models
#user, history, query
# https://pypi.org/project/looker-sdk/

def get_table_json(sysActivityTable: str):
    sql_query = models.SqlQueryCreate(
        model_name='system__activity',
        sql=f'select * from {sysActivityTable}'
        )

    created_query = sdk.create_sql_query(
        body=sql_query
        )
    run_query = sdk.run_sql_query(slug=created_query.slug, result_format='json')

    return run_query


if __name__ == "__main__":
    ini_file = '/usr/local/google/home/hugoselbie/code_sample/py/projects/ini/looker.ini'
    sdk = looker_sdk.init31(config_file=ini_file)

    # example usage
    data = get_table_json('history')
    print(data)
