from textual.theme import Theme

cynosure_theme = Theme(
    name="cynosure",
    primary="#e8e1c1",
    secondary="#ff0000",
    accent="#ff0000",
    foreground="#beb986",
    background="#112835",
    success="#beb986",
    warning="#EBCB8B",
    error="#ff0000",
    surface="#3B4252",
    panel="#434C5E",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)