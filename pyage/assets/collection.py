import random
from typing import Generic, List, Optional, Type, TypeVar, cast

from pyage.assets.asset import Asset
from pyage.assets.buffer import Buffer

T = TypeVar("T", bound=Asset)


class AssetCollection(Generic[T]):

    _asset_type: Type[T]
    _assets: List[Optional[T]]
    _buffers: List[Buffer]

    def __init__(self, buffers: List[Buffer], asset_type: Type[T]):
        self._buffers = buffers
        self._assets = [None] * len(buffers)
        self._asset_type = asset_type

    def get(self, cached: Optional[bool] = None) -> T:

        asset: T
        i = random.randrange(len(self._buffers))

        if cached is False:
            asset = self._asset_type(self._buffers[i])
        elif cached is True:
            if self._assets[i]:
                asset = cast(T, self._assets[i])
            else:
                asset = self._asset_type(self._buffers[i])
                self._assets[i] = asset
        else:
            return self.get(cached=self._asset_type._prefer_caching)

        asset.load(cached)

        return asset
