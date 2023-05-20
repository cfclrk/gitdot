THEMES: dict = {
    "none": {
        "graph_defaults": {},
        "node_defaults": {},
        "edge_defaults": {},
        "commit": {},
        "heads": {},
        "tags": {},
        "remotes": {},
        "default": {},
    },
    "dark": {
        "graph_defaults": {"bgcolor": "transparent"},
        "node_defaults": {"style": "filled", "fontsize": "14.0"},
        "edge_defaults": {"color": "darkorange", "arrowtail": "normal"},
        "commit": {"color": "bisque"},
        "heads": {"color": "lightblue", "shape": "box", "height": 0.2},
        "tags": {"color": "thistle", "shape": "box", "height": 0.2},
        "remotes": {"color": "green", "shape": "box", "height": 0.2},
        "default": {"color": "red", "shape": "box", "height": 0.2},
    },
    "light": {},
}


LOG_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "stdoutFormatter": {
            "format": "// %(levelname)s %(filename)s:%(lineno)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "stdoutFormatter",
        },
    },
    "loggers": {
        "gitdot": {"handlers": ["console"], "level": "ERROR", "propagate": True}
    },
}
