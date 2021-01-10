# About the decorations

Each decoration is stored in a separate folder and contains two main files:

-   `decoration.png` - The decoration itself. pasted on top of the profile image.
-   `mask.png` - A grayscale image that is used as a mask to the profile picture.

If a decoration doesn't contain the `mask.png` file, it will be loaded from
the [default](/default) decoration.
If a decoration doesn't have a `decoration.png` file, will use a transparent
image as the decoration.

The profile picture will always be placed in **the center** of the decoration
image, and the size of the profile picture will always be 256x256px.
