""" esto hacerlo un archivo sh """

import sys

from utils.management.project_management_utility import ProjectManagementUtility
from utils.management.help_management_utility import HelpManagementUtility

if __name__ == "__main__":
    help_mu = HelpManagementUtility
    try:
        com = sys.argv[1]
        if com == "new":
            project_mu = ProjectManagementUtility(sys.argv[2], sys.argv[3])
            project_mu.generate_project()
        if com == "help":
            help_mu.help()
    except IndexError as e:
        print(e)
        help_mu.help()

        