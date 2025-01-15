from collective.hardening import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface
from zope.interface import implementer
from z3c.form.object import registerFactoryAdapter
from plone.registry.field import PersistentField


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


class IStrictTransportSecurity(Interface):

    enabled = schema.Bool(
        title=_("label_enabled", default="Enabled"),
        description=_(
            "description_enabled",
            default="Enable the Strict-Transport-Security header.",
        ),
        required=False,
        default=False,
    )

    max_age = schema.Int(
        title=_("label_max_age", default="Max Age"),
        description=_(
            "description_max_age",
            default="The time in seconds that the browser should remember that this site is only to be accessed using HTTPS.",
        ),
        required=True,
        min=0,
        default=31536000,
    )

    include_subdomains = schema.Bool(
        title=_("label_include_subdomains", default="Include Subdomains"),
        description=_(
            "description_include_subdomains",
            default="If enabled, the rule applies to all of the site's subdomains as well.",
        ),
        required=False,
        default=False,
    )

    preload = schema.Bool(
        title=_("label_preload", default="Preload"),
        description=_(
            "description_preload",
            default="If enabled, the site is included in the HSTS preload list.",
        ),
        required=False,
        default=False,
    )


@implementer(IStrictTransportSecurity)
class StrictTransportSecurity:

    def __init__(self, enabled=False, max_age=31536000, include_subdomains=False, preload=False):
        self.enabled = enabled
        self.max_age = max_age
        self.include_subdomains = include_subdomains
        self.preload = preload


registerFactoryAdapter(IStrictTransportSecurity, StrictTransportSecurity)

class StrictTransportSecurityField(PersistentField, schema.Object):
    pass

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

    strict_transport_security = StrictTransportSecurityField(
        title=_("label_strict_transport_security", default="Strict Transport Security"),
        description=_(
            "description_strict_transport_security",
            default="Control the Strict-Transport-Security header settings.",
        ),
        schema=IStrictTransportSecurity,
        required=False,
    )

class HardeningEditForm(RegistryEditForm):
    schema = IHardeningSettings
    schema_prefix = "collective.hardening.settings"
    label = _("Hardening settings")
    description = _("Control panel to setup the hardening settings for the site.")


HardeningControlPanel = layout.wrap_form(HardeningEditForm, ControlPanelFormWrapper)
