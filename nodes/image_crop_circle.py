import numpy as np
from PIL import Image, ImageDraw


class ImageCropCircle:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "crop_circle"

    CATEGORY = "image/crop"

    def crop_circle(self, image):
        width, height = image.size
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, width, height), fill=255)
        result = Image.new("RGBA", (width, height))
        result.paste(image, (0, 0), mask)
        return (result,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ImageCropCircle": ImageCropCircle,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCropCircle": "ImageCropCircle",
}
