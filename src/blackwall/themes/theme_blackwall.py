from textual.theme import Theme

blackwall_theme = Theme(
    name="blackwall",
    primary="#a11616",
    secondary="#ff0000",
    accent="#ff0000",
    foreground="#E8E8E8",
    background="#1D1D1D",
    success="#1AAD00",
    warning="#CA9200",
    error="#ff0000",
    surface="#282828",
    panel="#939393",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#353535",
        "input-selection-background": "#81a1c1 35%",
    },
)