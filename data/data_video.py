import os
import os.path
import random
from typing import Callable, cast, Dict, List, Optional, Tuple

from torchvision.datasets.folder import has_file_allowed_extension

def make_dataset(
    directory: str,
    class_to_idx: Dict[str, int],
    flod: int,
    extensions: Optional[Tuple[str, ...]] = None,
    is_valid_file: Optional[Callable[[str], bool]] = None,
) -> List[Tuple[str, int]]:
    instances = []
    directory = os.path.expanduser(directory)
    both_none = extensions is None and is_valid_file is None
    both_something = extensions is not None and is_valid_file is not None
    if both_none or both_something:
        raise ValueError("Both extensions and is_valid_file cannot be None or not None at the same time")
    if extensions is not None:
        def is_valid_file(x: str) -> bool:
            return has_file_allowed_extension(x, cast(Tuple[str, ...], extensions))
    is_valid_file = cast(Callable[[str], bool], is_valid_file)
    for target_class in sorted(class_to_idx.keys()):
        class_index = class_to_idx[target_class]
        target_dir = os.path.join(directory, target_class)
        if not os.path.isdir(target_dir):
            continue
        for root, _, fnames in sorted(os.walk(target_dir, followlinks=True)):
            fnames_len = len(fnames) // flod
            fnames_idx = random.sample(range(len(fnames)), len(fnames) // flod)
            # for fname in sorted(fnames):
            for i in range(fnames_len):
                fname = fnames[fnames_idx[i]]
                path = os.path.join(root, fname)
                if is_valid_file(path):
                    item = path, class_index
                    instances.append(item)

    return instances