# src/utils/permissions.py

APPLICATION_MODULES = [
    "Settings",
    "Team",
    "Projects",
    "Tasks",
]

PERMISSION_DEFINITIONS = [
    # Settings
    {"key": "view_settings", "label": "View Settings", "description": "View the settings page", "group": "Settings"},
    {"key": "edit_settings", "label": "Edit Settings", "description": "Modify settings", "group": "Settings"},

    # Team - page level
    {"key": "view_team_page", "label": "View Team Page", "description": "Access the team page", "group": "Team"},

    # Team - Members tab
    {"key": "view_members", "label": "View Members", "description": "See team members", "group": "Team"},
    {"key": "create_members", "label": "Create Members", "description": "Invite/add new members", "group": "Team"},
    {"key": "edit_members", "label": "Edit Members", "description": "Update member details", "group": "Team"},
    {"key": "delete_members", "label": "Delete Members", "description": "Remove a member", "group": "Team"},
    {"key": "activate_deactivate_members", "label": "Activate / Deactivate Members", "description": "Change a member's status", "group": "Team"},

    # Team - Roles tab
    {"key": "view_roles", "label": "View Roles", "description": "List all roles", "group": "Team"},
    {"key": "create_roles", "label": "Create Roles", "description": "Add new custom roles", "group": "Team"},
    {"key": "edit_roles", "label": "Edit Roles", "description": "Modify role permissions", "group": "Team"},
    {"key": "delete_roles", "label": "Delete Roles", "description": "Remove roles permanently", "group": "Team"},

    # Projects
    {"key": "view_projects", "label": "View Projects", "description": "See all projects", "group": "Projects"},
    {"key": "create_projects", "label": "Create Projects", "description": "Create new projects", "group": "Projects"},
    {"key": "edit_projects", "label": "Edit Projects", "description": "Modify existing projects", "group": "Projects"},
    {"key": "delete_projects", "label": "Delete Projects", "description": "Permanently remove projects", "group": "Projects"},
    {"key": "add_project_members", "label": "Add Project Members", "description": "Add members to a project", "group": "Projects"},

    # Tasks
    {"key": "view_tasks", "label": "View Tasks", "description": "View the tasks page", "group": "Tasks"},
    {"key": "create_tasks", "label": "Create Tasks", "description": "Create new tasks", "group": "Tasks"},
    {"key": "edit_tasks", "label": "Edit Tasks", "description": "Modify existing tasks", "group": "Tasks"},
    {"key": "delete_tasks", "label": "Delete Tasks", "description": "Permanently remove tasks", "group": "Tasks"},
]

AVAILABLE_PERMISSIONS = [p["key"] for p in PERMISSION_DEFINITIONS]


def get_permission_def(key: str) -> dict:
    return next((p for p in PERMISSION_DEFINITIONS if p["key"] == key), {
        "key": key, "label": key, "description": "", "group": "",
    })


def get_module_keys(group: str) -> list[str]:
    return [p["key"] for p in PERMISSION_DEFINITIONS if p["group"] == group]