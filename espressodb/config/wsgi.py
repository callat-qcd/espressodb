"""
WSGI config for espressodb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
import time
import traceback
import signal

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "espressodb.config.settings")


def main():
    """Launches the applications and catches "mod_wsgi" errors.
    """
    try:
        get_wsgi_application()
        print("WSGI without exception")
    except Exception as e:  # pylint: disable=W0703
        print("handling WSGI exception")
        print(e)
        # Error loading applications
        if "mod_wsgi" in sys.modules:
            traceback.print_exc()
            os.kill(os.getpid(), signal.SIGINT)
            time.sleep(2.5)


if __name__ == "__main__":
    main()
