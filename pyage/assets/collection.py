import random
from typing import Generic, List, TypeVar

from pyage.assets.asset import Asset

T = TypeVar("T", bound=Asset)


class AssetCollection(Generic[T]):

    _assets: List[T]

    def __init__(self, assets: List[T]):
        self._assets = assets

    def get(self) -> T:

        asset: T = random.choice(self._assets)

        asset.load()

        return asset
