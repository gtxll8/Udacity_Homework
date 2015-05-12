# config.py

from authomatic.providers import oauth2, oauth1
import authomatic


CONFIG = {

    'tw': { # Your internal provider name

        # Provider class
        'class_': oauth1.Twitter,

        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': 'wM0LNsBC6W0VOwIEaZuMxsP5d',
        'consumer_secret': 'aXtrzZHC3kbQKHsm0EX9DnvIOJeg8ZugU8o1IP2txDjnM6YG2K',
    },

        'github': { # Your internal provider name

        # Provider class
        'class_': oauth2.GitHub,

        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': '2cb3423c3307604727e0',
        'consumer_secret': 'efe045296c5e8763a9ab0cc6eac36a7718ca6f77',
        'access_headers': {'User-Agent': 'Awesome-Octocat-App'},
    },

    'fb': {

        'class_': oauth2.Facebook,

        # Facebook is an AuthorizationProvider too.
        'consumer_key': '########################',
        'consumer_secret': '########################',

        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'publish_stream'],
    },

    'google': {
        'class_': oauth2.Google,
        'consumer_key': '720789354184-aokdhm5b8m2bjk6vtsb1aal83p1u0pgv.apps.googleusercontent.com',
        'consumer_secret': 'dW3onhfvmsEIKXWq668OJdK1',
        'id': authomatic.provider_id(),
        'scope': oauth2.Google.user_info_scope + [
            'email',
            'https://www.googleapis.com/auth/calendar',
            'https://mail.google.com/mail/feed/atom',
            'https://www.googleapis.com/auth/drive',
            'https://gdata.youtube.com'],
        '_apis': {
            'List your calendars': ('GET', 'https://www.googleapis.com/calendar/v3/users/me/calendarList'),
            'List your YouTube playlists': ('GET', 'https://gdata.youtube.com/feeds/api/users/default/playlists?alt=json'),
            },
    },

}
