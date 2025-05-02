from textual.theme import Theme

legacy_3270_theme = Theme(
    name="LEGACY 3270",
    primary="#00feff",
    secondary="#17f9e1",
    accent="#ff0000",
    foreground="#f3ebdb",
    background="#000000",
    success="#0efd03",
    warning="#f5ff30",
    error="#ff0000",
    surface="#000000",
    panel="#0efd03",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
        "border": "#17f9e1",
        "border-blurred": "#17f9e1",
        "footer-foreground": "#000000",
        "footer-description-foreground": "#000000",
        "button-foreground": "",
    },
)