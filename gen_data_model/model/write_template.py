# -*- coding: UTF-8 -*-

"""
 Module
     write_template.py
 Copyright
     Copyright (C) 2018 Vladimir Roncevic <elektron.ronca@gmail.com>
     gen_data_model is free software: you can redistribute it and/or modify it
     under the terms of the GNU General Public License as published by the
     Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.
     gen_data_model is distributed in the hope that it will be useful, but
     WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
     See the GNU General Public License for more details.
     You should have received a copy of the GNU General Public License along
     with this program. If not, see <http://www.gnu.org/licenses/>.
 Info
     Define class WriteTemplate with attribute(s) and method(s).
     Write a template content with parameters to a file.
"""

import sys
from datetime import date
from os import getcwd, chmod
from string import Template
from inspect import stack

try:
    from gen_data_model.model.model_selector import ModelSelector
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_bad_call_error import ATSBadCallError
except ImportError as error:
    MESSAGE = "\n{0}\n{1}\n".format(__file__, error)
    sys.exit(MESSAGE)  # Force close python ATS ##############################

__author__ = "Vladimir Roncevic"
__copyright__ = "Copyright 2018, Free software to use and distributed it."
__credits__ = ["Vladimir Roncevic"]
__license__ = "GNU General Public License (GPL)"
__version__ = "1.0.0"
__maintainer__ = "Vladimir Roncevic"
__email__ = "elektron.ronca@gmail.com"
__status__ = "Updated"


class WriteTemplate(object):
    """
        Define class WriteTemplate with attribute(s) and method(s).
        Write a template content with parameters to a file.
        It defines:

            :attributes:
                | __slots__ - Setting class slots
                | __check_status - Check status
                | VERBOSE - Console text indicator for current process-phase
            :methods:
                | __init__ - Initial constructor
                | get_check_status - Getter for check status
                | write - Write a template content with parameters to a file
    """

    __slots__ = ('VERBOSE', '__check_status')
    VERBOSE = 'GEN_DATA_MODEL::MODEL::WRITE_TEMPLATE'

    def __init__(self, verbose=False):
        """
            Initial constructor.

            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :excptions: None
        """
        verbose_message(
            WriteTemplate.VERBOSE, verbose, 'Initial writer'
        )
        self.__check_status = False

    def get_check_status(self):
        """
            Getter for check status.

            :return: Getting check status
            :rtype: <bool>
            :excptions: None
        """
        return self.__check_status

    def write(self, model_content, model_name, verbose=False):
        """
            :param model_content: Template content for model.

            :type model_content: <str>
            :param model_name: Parameter model name
            :type model_name: <str>
            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :return: Boolean status
            :rtype: <bool>
            :excptions: ATSBadCallError | ATSTypeError
        """
        func, status, file_name = stack()[0][3], False, None
        model_cont_txt = 'Argument: expected model_content <str> object'
        model_cont_msg = "{0} {1} {2}".format('def', func, model_cont_txt)
        model_name_txt = 'Argument: expected model_content <str> object'
        model_name_msg = "{0} {1} {2}".format('def', func, model_name_txt)
        if model_content is None or not model_content:
            raise ATSBadCallError(model_cont_msg)
        if not isinstance(model_content, str):
            raise ATSTypeError(model_cont_msg)
        if model_name is None or not model_name:
            raise ATSBadCallError(model_name_msg)
        if not isinstance(model_name, str):
            raise ATSTypeError(model_name_msg)
        verbose_message(WriteTemplate.VERBOSE, verbose, 'Writer template')
        self.__check_status = True
        file_name = ModelSelector.format_name(model_name)
        if file_name:
            current_dir = getcwd()
            module_file = "{0}/{1}".format(current_dir, file_name)
            model_params = {
                'mod': "{0}".format(model_name),
                'modlc': "{0}".format(model_name.lower()),
                'date': "{0}".format(date.today()),
                'year': "{0}".format(date.today().year)
            }
            template = Template(model_content)
            verbose_message(
                WriteTemplate.VERBOSE, verbose, 'Write data model', module_file
            )
            if template:
                with open(module_file, 'w') as model_file:
                    model_file.write(template.substitute(model_params))
                    chmod(module_file, 0o666)
                    status = True
        return True if status else False
