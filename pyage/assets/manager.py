import fnmatch
import pathlib
from typing import Dict, Generator, List, Optional, Sequence, Type, TypeVar, Union

from pysingleton import PySingleton

from pyage.assets.asset import Asset
from pyage.assets.buffer import Buffer
from pyage.assets.collection import AssetCollection
from pyage.assets.file_buffer import FileBuffer
from pyage.exceptions import AssetAlreadyLoadedError

T = TypeVar("T", bound=Asset)


class AssetManager(metaclass=PySingleton):
    """
    The asset manager allows you to load assets via the
    :meth:`~pyage.assets.AssetManager.load` method, after which you can access
    the loaded assets by calling the
    :meth:`~pyage.assets.AssetManager.get` method. This will return
    a :class:`pyage.assets.AssetCollection` object, which can hold an unlimited
    amount of assets from which you can request one at any time to work with it.

    The usual assets workflow goes like this:

    1. When loading the game, e.g. before calling :meth:`pyage.App.process`,
       load all assets by calling :meth:`~pyage.assets.AssetManager.load` as
       often as you need. This will make sure that the buffers are known
       whenever you need the actual asset.
    2. Whenever you want to access an asset, call
       :meth:`~pyage.assets.AssetManager.get` with the specific asset type (e.g.
       :class:`pyage.assets.Sound`) and the asset name. The name can also
       be a wildcard pattern, in which case multiple assets will be returned
       within the :class:`pyage.assets.AssetCollection` that gets returned. To
       finally access the assets within that collection, call
       :meth:`pyage.assets.AssetCollection.get` to get a random asset from
       within the collection. This asset will then have all features provided
       by the specific asset type you provided when calling
       :meth:`pyage.assets.AssetManager.get`. That flexible system allows you
       to implement own asset types for your specific game (more on that will
       be featured in the documentation later).

    The asset manager is a singleton class, you thus don't need to store it
    somewhere, it will be kept alive by the framework.
    """

    _buffers: Dict[str, Buffer]
    _source_path: pathlib.Path

    def __init__(self) -> None:

        self._buffers = {}
        self._source_path = pathlib.Path(".").resolve()

    def load(
        self,
        assets: Sequence[str],
        lazy: bool = True,
    ) -> None:
        """
        loads assets to be retrieved and used later via
        :meth:`~pyage.assets.AssetManager.get`

        Parameters
        ----------
        assets

            a list of specifiers which will be used to search for assets. A
            specifier may be a file name without the
            :attr:`~pyage.assets.AssetManager.source_path` prefix. You can
            however use glob patterns to search for multiple files at once.

            .. code-block:: python

               from pyage.assets import AssetManager

               # this will load all files starting with sword-hit_
               AssetManager().load(['sword-hit_*'])

        lazy

            defines if the buffers for the assets should be loaded right at
            this moment (lazy=False), or as soon as an asset is actually
            retrieved for use from the asset collection (lazy=True). This can
            be used to control the behaviour of the game (slow or fast startup,
            wait time before loading maps etc).
        """

        buffer: Buffer
        p: pathlib.Path

        for asset in assets:

            found: Generator[pathlib.Path, None, None] = self._source_path.glob(asset)

            for p in found:

                if not p.is_file():
                    continue

                if str(p.resolve()) in self._buffers:
                    raise AssetAlreadyLoadedError(
                        f"this asset is already loaded: {p.resolve()}"
                    )

                buffer = FileBuffer(p)

                if not lazy:
                    buffer.load()

                self._buffers[str(p.resolve())] = buffer

    def get(self, type: Type[T], name: str) -> Optional[AssetCollection[T]]:
        """
        Retrieve an asset collection which contains one or more assets
        previously loaded via :meth:`~pyage.assets.AssetManager.load`.

        Parameters
        ----------
        type

            an asset type (e.g. :class:`pyage.assets.Sound`), which will be the
            asset type contained within the returned asset collection. An asset
            collection can only contain one specific type of assets which you
            need to specify here beforehand. That allows you to reuse the same
            loaded asset for multiple different asset types (e.g. a 3D or a
            regularly panned sound etc).

        name

            a specifier like in :meth:`~pyage.assets.AssetManager.load`.
            If a glob pattern is used, the returned asset collection will
            contain all matching assets.
        """

        if name in self:

            name = str((self._source_path / name).resolve())

            found: List[str] = fnmatch.filter(self._buffers.keys(), name)

            return AssetCollection([type(self._buffers[n]) for n in found])

        return None

    @property
    def source_path(self) -> pathlib.Path:
        """
        the source path is the path where the
        :meth:`~pyage.asset_manager.AssetManager.load` method will look by default
        when searching for a specific asset to load. The default is the
        working directory of the current app.

        Raises
        ------
        :exc:`AttributeError`

            either you cannot change the source path after assets are already
            loaded, the given path does not exist or the path doesn't point to
            a directory

        :exc:`TypeError`

            path parameter has invalid type
        """

        return self._source_path

    @source_path.setter
    def source_path(self, path: Union[str, pathlib.Path]) -> None:

        temp: pathlib.Path

        if len(self._buffers) > 0:
            raise AttributeError(
                "the source path cannot be modified when assets are already loaded"
            )

        if isinstance(path, str):
            temp = pathlib.Path(path)
        elif isinstance(path, pathlib.Path):
            temp = path
        else:
            raise TypeError("path attribute must be a pathlib.Path or str")

        if not temp.exists():
            raise AttributeError("the given path doesn't exist")

        if not temp.is_dir():
            raise AttributeError("the given path doesn't point to a directory")

        self._source_path = temp

    def __contains__(self, name: str) -> bool:

        if not isinstance(name, str):
            return False

        name = str((self._source_path / name).resolve())

        found: List[str] = fnmatch.filter(self._buffers.keys(), name)

        if len(found) > 0:
            return True

        return False
