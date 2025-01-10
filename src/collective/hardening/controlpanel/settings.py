from collective.hardening import _
from plone.app.registry.browser import controlpanel
from zope import schema
from zope.interface import Interface


class IHardeningSettings(Interface):
    """Global settings for collective.hardening.

    This describes records stored in the configuration registry and
    obtainable via plone.registry.
    """

    mimetypes_deny_list = schema.List(
        title=_("label_mimetypes_deny_list", default="Denied Mimetypes"),
        description=_(
            "description_mimetypes_deny_list",
            default="Specify the list of mimetypes to be denied on the site. Use '*' as a wildcard to match multiple mimetypes.",
        ),
        value_type=schema.TextLine(),
        required=False,
    )

    extensions_deny_list = schema.List(
        title=_("label_extensions_deny_list", default="Denied Extensions"),
        description=_(
            "description_extensions_deny_list",
            default="Specify the list of file extensions to be denied on the site. The check is case-insensitive.",
        ),
        value_type=schema.TextLine(),
        required=False,
    )


class HardeningEditForm(controlpanel.RegistryEditForm):
    schema = IHardeningSettings
    schema_prefix = "collective.hardening.settings"
    label = _("Hardening settings")
    description = _("Control panel to setup the hardening settings for the site.")


class HardeningControlPanel(controlpanel.ControlPanelFormWrapper):
    form = HardeningEditForm
