from authomatic.providers import oauth2, oauth1
import authomatic


CONFIG = {

    'tw': { # Your internal provider name

        # Provider class
        'class_': oauth1.Twitter,

        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': 'xxxxxxxxxxxxxxxxxxxxxxx',
        'consumer_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    },

    'github': { # Your internal provider name

        # Provider class
        'class_': oauth2.GitHub,

        # GitHub is an AuthorizationProvider too, so we need to set several other properties again:
        'consumer_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'consumer_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'access_headers': {'User-Agent': 'Awesome-Octocat-App'},
        'scope': ['id', 'email', 'name'],
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
        'consumer_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com',
        'consumer_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1',
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
