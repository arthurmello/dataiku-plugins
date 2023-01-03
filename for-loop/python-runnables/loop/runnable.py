#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is the actual code for the Python runnable for loop
import dataiku
from dataiku.runnables import Runnable

class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        # Retrieve macro parameters:
        variable = self.config.get("variable")
        liste_valeurs = self.config.get("liste_valeurs")
        scenario = self.config.get("scenario")
        
        # Retrieve project parameters
        #project = dataiku.api_client().get_project(dataiku.default_project_key())
        client = dataiku.api_client()
        project = client.get_project(self.project_key)
        variables = project.get_variables()
        scenario_maj = project.get_scenario(scenario)
        
        liste_valeurs = liste_valeurs.split(',')
        
        for valeur in liste_valeurs:
            # Update variable
            variables['standard'][variable] = valeur
            project.set_variables(variables)
            
            # Run scenario
            scenario_maj.run_and_wait()
        
        result = u"<html>The macro has run successfully! <br> \
                    Scenario run: {scenario}<br> \
                    Variable updated: {variable} <br> \
                    Values set for the variable: {liste_valeurs}</html>".format(
            scenario=scenario, variable=variable, liste_valeurs=', '.join(liste_valeurs))
        
        return result
        