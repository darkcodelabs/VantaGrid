"""Image viewer widget for displaying images in the terminal."""
from __future__ import annotations

from pathlib import Path
from textual.widgets import Static
from rich.text import Text


class ImageViewer(Static):
    """Display images in the terminal using colored half-block characters."""

    DEFAULT_CSS = """
    ImageViewer {
        height: 1fr;
        width: 1fr;
        overflow: auto;
    }
    """

    def __init__(self, path: Path | str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.path = Path(path) if path else None

    def on_mount(self) -> None:
        """Load image on mount if path is provided."""
        if self.path:
            self.load_image(self.path)

    def load_image(self, path: Path | str) -> None:
        """Load and display an image.

        Args:
            path: Path to the image file
        """
        self.path = Path(path) if isinstance(path, str) else path

        try:
            from PIL import Image
        except ImportError:
            self.update(
                "[bold red]Image Viewer Error[/]\n"
                "Install Pillow to view images:\n"
                "[yellow]pip install Pillow[/]"
            )
            return

        try:
            # Load image
            img = Image.open(self.path)

            # Convert to RGB if necessary
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Get terminal width (approximate character width)
            # Most terminals are 80 chars wide, use smaller width for safety
            terminal_width = 60
            aspect_ratio = img.height / img.width

            # Each character cell is roughly 2x1 in pixel ratio
            # For half-blocks (▀▄), we need 2 height units per character
            new_width = terminal_width
            new_height = int(terminal_width * aspect_ratio * 0.5)

            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to half-block display
            pixels = img.load()
            output_lines = []

            for y in range(0, new_height - 1, 2):
                line = Text()
                for x in range(new_width):
                    # Get two pixels vertically
                    top_pixel = pixels[x, y]
                    bottom_pixel = pixels[x, y + 1]

                    # Convert RGB to terminal color
                    top_color = self._rgb_to_hex(top_pixel)
                    bottom_color = self._rgb_to_hex(bottom_pixel)

                    # Use half-block character (▀) with top color foreground
                    # and bottom color background
                    char = "▀"
                    line.append(char, style=f"{top_color} on {bottom_color}")

                output_lines.append(line)

            # Combine all lines into a Text object
            result = Text()
            for i, line in enumerate(output_lines):
                result.append_text(line)
                if i < len(output_lines) - 1:
                    result.append("\n")

            self.update(result)

        except Exception as e:
            self.update(f"[bold red]Error loading image:[/]\n{str(e)}")

    @staticmethod
    def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color code.

        Args:
            rgb: Tuple of (R, G, B) values

        Returns:
            Hex color code as string
        """
        r, g, b = rgb
        return f"#{r:02x}{g:02x}{b:02x}"
