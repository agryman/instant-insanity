import base64
import mimetypes
from importlib.resources import files
from IPython.display import HTML, Image

IMAGES_PACKAGE: str = "instant_insanity.resources.images"


def show_image(subpackage: str, filename: str, **kwargs) -> Image:
    """
    The function creates an HTML <img> element with a data URL and attributes given by kwargs.
    Args:
        subpackage: The subpackage name or the empty string.
        filename: The image filename.
        **kwargs: Optional <img> attributes.

    Returns:

    """
    package: str = IMAGES_PACKAGE
    if len(subpackage) > 0:
        package = package + "." + subpackage
    res = files(package) / filename
    return Image(data=res.read_bytes(), **kwargs)


def show_div_image(subpackage: str, filename: str, width: str = "75%", alt: str = "") -> HTML:
    """
    The function creates a centered HTML <img> element wrapped in a <div>, using a data URL.

    Args:
        subpackage: The subpackage name or the empty string.
        filename: The image filename.
        width: The CSS width of the image, e.g. "75%". Defaults to "75%".
        alt: The alt text for the image. Defaults to "".

    Returns:
        An IPython HTML object containing the centered image.
    """
    package: str = IMAGES_PACKAGE
    if len(subpackage) > 0:
        package = package + "." + subpackage
    res = files(package) / filename
    data: bytes = res.read_bytes()
    mime: str = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    b64: str = base64.b64encode(data).decode()
    html: str = (
        f'<div style="text-align: center;">'
        f'<img src="data:{mime};base64,{b64}" alt="{alt}" style="width: {width};">'
        f'</div>'
    )
    return HTML(html)
