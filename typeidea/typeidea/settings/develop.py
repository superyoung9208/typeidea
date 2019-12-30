from .base import *  # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += [
    # 'debug_toolbar',
    # 'debug_toolbar_line_profiler',
    # 'pympler',

]

INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_PANELS = [
    # 'djdt_flamegraph.FlamegraphPanel'  # 火焰图分析
    # 'pympler.panels.MemoryPanel'  # 内存占用分析
    # 'debug_toolbar_line_profiler.panel.ProfilingPanel'
]
