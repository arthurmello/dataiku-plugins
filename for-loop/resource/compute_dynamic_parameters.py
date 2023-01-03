import dataiku
def do(payload, config, plugin_config, inputs):
    client = dataiku.api_client()
    project_key = dataiku.default_project_key()
    project = client.get_project(project_key)
    variables = project.get_variables()['standard']
    scenarios = [s[u'id'] for s in project.list_scenarios()]
    
    
    if payload.get('parameterName') == 'variable':
        choices = [
            {"value" : v, "label" : v} for v in variables
        ]
        
        return {"choices": choices}

    if payload.get('parameterName') == 'scenario':
        choices = [
            {"value" : s, "label" : s} for s in scenarios
        ]
        return {"choices": choices}