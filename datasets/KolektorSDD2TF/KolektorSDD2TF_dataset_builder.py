"""KolektorSDD2TF dataset."""

import tensorflow_datasets as tfds
import numpy as np
import cv2
import os

class Builder(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for KolektorSDD2TF dataset."""

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    # Specifies the tfds.core.DatasetInfo object
    return self.dataset_info_from_configs(
        features=tfds.features.FeaturesDict({
            # These are the features of your dataset like images, labels ...
            'image': tfds.features.Image(shape=(None, None, 3)),
            'label': tfds.features.ClassLabel(names=['no', 'yes']),
            'labeledImage': tfds.features.LabeledImage(labels=['OK', 'defect'], shape=(None, None, 1)),
        }),
        # If there's a common (input, target) tuple from the
        # features, specify them here. They'll be used if
        # `as_supervised=True` in `builder.as_dataset`.
        supervised_keys=('image', 'label', 'labeledImage'),  # Set to `None` to disable
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    # Downloads the data and defines the splits
    path = dl_manager.download_and_extract('https://go.vicos.si/kolektorsdd2')
    # Returns the Dict[split names, Iterator[Key, Example]]
    return {
        'train': self._generate_examples(path / 'train'),
        'test': self._generate_examples(path / 'test'),
    }

  def _generate_examples(self, path):
    """Yields examples."""
    # Yields (key, example) tuples from the dataset
    for img_GT in path.glob('*_GT.png'):
      key = img_GT.stem.split('_')[0]
      label = 1 if cv2.imread(str(img_GT)).any() else 0 # check if defect exists

      yield key, {
          'image': path / f'{key}.png',
          'label': label,
          'labeledImage': path / f'{key}_GT.png',
      }
