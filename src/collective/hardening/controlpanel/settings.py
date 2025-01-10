from collective.hardening import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


def _default_mimetypes_deny_list():
    """
    Returns a set of mimetypes that should be denied for upload.
    """
    return {
        "application/javascript",  # JavaScript files
        "application/octet-stream",  # Generic binary files
        "application/x-*",  # Catch-all for executables
    }


def _default_extensions_deny_list():
    """
    Returns a set of file extensions that should be denied for upload.
    """
    return {
        "asp",  # Active Server Pages files
        "aspx",  # Active Server Pages files
        "bat",  # Batch script files
        "cmd",  # Command script files
        "com",  # DOS command files
        "dll",  # Dynamic link library files
        "exe",  # Executable files
        "jar",  # Java archive files
        "jsp",  # JavaServer Pages files
        "msi",  # Windows installer files
        "ps1",  # PowerShell scripts
        "scr",  # Screensaver files (executable)
        "sh",  # Shell script files
        "vbs",  # VBScript files
    }


class IHardeningSettings(Interface):
    """Global settings for collective.hardening.

    This describes records stored in the configuration registry and
    obtainable via plone.registry.
    """

    mimetypes_deny_list = schema.Set(
        title=_("label_mimetypes_deny_list", default="Denied Mimetypes"),
        description=_(
            "description_mimetypes_deny_list",
            default="Specify the list of mimetypes to be denied on the site. Use '*' as a wildcard to match multiple mimetypes.",
        ),
        value_type=schema.TextLine(),
        required=False,
        defaultFactory=_default_mimetypes_deny_list,
    )

    extensions_deny_list = schema.Set(
        title=_("label_extensions_deny_list", default="Denied Extensions"),
        description=_(
            "description_extensions_deny_list",
            default="Specify the list of file extensions to be denied on the site. The check is case-insensitive.",
        ),
        value_type=schema.TextLine(),
        required=False,
        defaultFactory=_default_extensions_deny_list,
    )


class HardeningEditForm(RegistryEditForm):
    schema = IHardeningSettings
    schema_prefix = "collective.hardening.settings"
    label = _("Hardening settings")
    description = _("Control panel to setup the hardening settings for the site.")


HardeningControlPanel = layout.wrap_form(HardeningEditForm, ControlPanelFormWrapper)
