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
        # Convert the input tensor to a PIL Image
        image = Image.fromarray(image.squeeze().permute(1, 2, 0).byte().numpy())

        width, height = image.size
        size = min(width, height)

        # Calculate offsets to center the crop
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size

        # Create a circular mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        # Ensure the image has an alpha channel
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # Crop and apply mask
        image = image.crop((left, top, right, bottom))
        result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        result.paste(image, (0, 0), mask)

        # Convert back to tensor format
        result_tensor = np.array(result).astype(np.float32) / 255.0
        result_tensor = np.moveaxis(result_tensor, -1, 0)
        return (result_tensor,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ImageCropCircle": ImageCropCircle,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCropCircle": "ImageCropCircle",
}
