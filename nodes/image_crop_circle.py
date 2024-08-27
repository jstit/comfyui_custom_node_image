import numpy as np
import torch


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
        # Get dimensions from the image
        _, h, w, _ = image.shape

        # Determine the size of the circle (use the smaller dimension)
        size = min(h, w)

        # Calculate the crop coordinates to center the circle
        x = (w - size) // 2
        y = (h - size) // 2

        # Crop the image to a square
        cropped = image[:, y : y + size, x : x + size, :]

        # Create a circular mask
        center = (size // 2, size // 2)
        radius = size // 2
        Y, X = np.ogrid[:size, :size]
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)
        mask = dist_from_center <= radius

        # Apply the mask
        mask = torch.from_numpy(mask).float().unsqueeze(0).unsqueeze(-1)
        mask = mask.expand_as(cropped)
        result = cropped * mask

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
