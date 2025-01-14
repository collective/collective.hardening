[![image](https://github.com/collective/collective.hardening/actions/workflows/plone-package.yml/badge.svg)](https://github.com/collective/collective.hardening/actions/workflows/meta.yml)
[![Coveralls](https://coveralls.io/repos/github/collective/collective.hardening/badge.svg?branch=main)](https://coveralls.io/github/collective/collective.hardening?branch=main)
[![image](https://codecov.io/gh/collective/collective.hardening/branch/master/graph/badge.svg)](https://codecov.io/gh/collective/collective.hardening)
[![Latest Version](https://img.shields.io/pypi/v/collective.hardening.svg)](https://pypi.python.org/pypi/collective.hardening/)
[![Egg Status](https://img.shields.io/pypi/status/collective.hardening.svg)](https://pypi.python.org/pypi/collective.hardening)
![image](https://img.shields.io/pypi/pyversions/collective.hardening.svg?style=plastic%20%20%20:alt:%20Supported%20-%20Python%20Versions)
[![License](https://img.shields.io/pypi/l/collective.hardening.svg)](https://pypi.python.org/pypi/collective.hardening/)

# collective.hardening

**collective.hardening** is an add-on designed to enhance Plone security by adding configurable features that help safeguard your site.

## Features

- **Dedicated Control Panel** Easily configure security-related settings from one central location.

- **File Type Restrictions** Control which file types (by extension or MIME type) can be uploaded to your site.

- **Additional Improvements (TDB)** Further enhancements are planned for upcoming releases.

### Control Panel

A new control panel, accessible at `/@@hardening-controlpanel`, allows you to fine-tune the add-on's security settings.
Through this interface, you can define which file types are permissible and ensure that only safe files are uploaded to your Plone site.
You can access the control panel under the **Security** section of the main Plone control panel.

### File Type Restrictions

Using the control panel, you can specify disallowed MIME types or file extensions. This flexibility helps prevent the upload of potentially harmful files, bolstering your site's security.

The implementation is based on:

1. Event subscribers active on created or modified objects.
2. A widget validator that checks the file type on upload.

## Installation

To install **collective.hardening**, add it to your buildout configuration as follows:

```ini
[instance]
eggs +=
    collective.hardening
```

After updating the configuration, run buildout:

```bash
bin/buildout
```

And restart your Plone instance.

## Authors

The [Syslab.com](https://www.syslab.com) team.

## Contributors

Put your name here, you deserve it!

- Alessandro Pisa, [Syslab.com](https://www.syslab.com)

## Contribute

- Issue Tracker: <https://github.com/collective/collective.hardening/issues>
- Source Code: <https://github.com/collective/collective.hardening>

## Support

If you are having issues, please let us know in the [issue tracker](https://github.com/collective/collective.hardening/issues).

## License

The project is licensed under the GPLv2.
