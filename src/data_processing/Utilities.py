import logging
import os
import sys
from pathlib import Path
from typing import List

import numpy as np
from numpy.typing import NDArray

from src.data_processing import EmbeddingFunctions
from src.data_processing import Filters
from src.data_processing import ImageGenerators
from src.data_processing import ImageProducts
from src.data_processing.ImageProducts import calculate_image_product_matrix

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def generate_filtered_image_set(imageType: str, filters: List[str], imageSetFilepath: str, overwrite=False) -> NDArray:
    """
    :param imageSetFilepath: Place where the image set was previously saved, or the place where the new image set should be saved
    :param overwrite: If true, generates and saves the filtered image set even if it is saved
    :return: An NDArray of filtered image sets as specified by imageType and filters
    Checks if such an image set is already saved in imageSetFilepath. If so it loads the image set
    If not, or if overridden, it uses the ImageGenerator and Filters module to generate a filtered image set
    """
    if not os.path.isfile(imageSetFilepath) or overwrite:
        logging.info("Image set not found/overwrite, generating filtered image set...")
        imageSet = ImageGenerators.get_image_set(imageType=imageType)

        logging.info("Image set generated, applying filters...")
        filteredImageSet = Filters.get_filtered_image_sets(imageSet=imageSet, filters=filters)

        # Creating the directory and saving the image set
        Path(imageSetFilepath).parent.mkdir(parents=True, exist_ok=True)
        np.save(imageSetFilepath, filteredImageSet)
    else:
        filteredImageSet = np.load(imageSetFilepath)
    return filteredImageSet


def generate_image_product_matrix(imageSet: NDArray, imageProductType: str, imageProductFilepath: str,
                                  overwrite=False) -> NDArray:
    """
    :param imageProductType: type of image product function to use
    :param imageSet: NDArray of images
    :param imageProductFilepath: Filepath to save/load the image product matrix
    :param overwrite: If true, generates and saves the image product table even if it is saved
    :return: An NDArray which is an image product matrix of the input filtered images and image product
    """
    if not os.path.isfile(imageProductFilepath) or overwrite:
        logging.info("Image product table not found/overwrite, generating image product table...")
        imageProduct = ImageProducts.get_image_product(imageProductType)
        imageProductMatrix = calculate_image_product_matrix(imageSet, imageProduct)

        # Creating the directory and saving the image product matrix
        Path(imageProductFilepath).parent.mkdir(parents=True, exist_ok=True)
        np.savetxt(imageProductFilepath, imageProductMatrix)
    else:
        imageProductMatrix = np.loadtxt(imageProductFilepath)
    return imageProductMatrix


def generate_embedding_matrix(imageProductMatrix, embeddingType, embeddingFilepath, overwrite=False):
    """
    :param imageProductMatrix: The image product matrix used to generate the vector embeddings
    :param embeddingType: Method used to generate the vector embeddings
    :param embeddingFilepath: Filepath to save/load the vector embeddings
    :param overwrite: If true, generates and saves the embeddings even if it is saved
    :return: The embedding matrix based on the inputs
    """
    if not os.path.isfile(embeddingFilepath) or overwrite:
        logging.info("Embedding matrix not found/overwrite. Generating embedding matrix...")
        embeddingMatrix = EmbeddingFunctions.get_embedding_matrix(imageProductMatrix, embeddingType)

        # Creating the directory and saving the embedding matrix
        Path(embeddingFilepath).parent.mkdir(parents=True, exist_ok=True)
        np.savetxt(embeddingFilepath, embeddingMatrix)
    else:
        embeddingMatrix = np.loadtxt(embeddingFilepath)
    return embeddingMatrix
