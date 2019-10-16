import sys

from clipio.utils import ProjectManagementUtility,MetadataManagementUtility, HelpManagementUtility

if __name__ == "__main__":
    help_mu = HelpManagementUtility
    
    try:
        command = sys.argv[1]
        if command == "new":
            project_mu = ProjectManagementUtility(sys.argv[2], sys.argv[3])
            project_mu.generate_project()
        if command == "help":
            help_mu.help()

    except IndexError:
        help_mu.help()



        